import graphene
from django.db import transaction
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.bases import Output
from graphql_auth.constants import Messages
from graphql_auth.exceptions import EmailAlreadyInUse
from graphql_auth.forms import RegisterForm
from graphql_auth.models import UserStatus
from graphql_auth.schema import UserNode
from graphql_jwt.decorators import token_auth

from .models import VerificationCode, User


class VerificationCodeType(DjangoObjectType):
    class Meta:
        model = VerificationCode


class GenerateVerificationCode(Output, graphene.Mutation):
    verification_code = graphene.Field(VerificationCodeType)

    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        if User.objects.filter(email=email).exists():
            return GenerateVerificationCode(success=False, errors={"email": Messages.EMAIL_IN_USE})

        return GenerateVerificationCode(verification_code=VerificationCode.generate_code(email))


class Register(Output, graphene.Mutation):
    user = graphene.Field(UserNode)
    token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)
        code = graphene.Int(required=True)

    @classmethod
    @token_auth
    def login_on_register(cls, root, info, **kwargs):
        return cls()

    def mutate(self, info, **kwargs):
        try:
            with transaction.atomic():
                f = RegisterForm(kwargs)
                if f.is_valid():
                    code = kwargs.get("code")
                    email = kwargs.get("email")
                    verification_code = VerificationCode.objects.filter(email=email).first()
                    if verification_code is None or verification_code.code != code:
                        return Register(success=False, errors={"code": "验证码错误"})

                    UserStatus.clean_email(email)
                    user = f.save()
                    user.status.verified = True
                    user.status.save()

                    payload = Register.login_on_register(
                        None, info, password=kwargs.get("password1"), **kwargs
                    )

                    return Register(success=True, user=user, token=getattr(payload, "token"))
                else:
                    return Register(success=False, errors=f.errors.get_json_data())
        except EmailAlreadyInUse:
            return Register(
                success=False,
                errors={"email": Messages.EMAIL_IN_USE},
            )


class AuthMutation(graphene.ObjectType):
    generate_verification_code = GenerateVerificationCode.Field()
    register = Register.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()
