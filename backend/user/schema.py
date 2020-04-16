import graphene
from django.db import transaction
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.bases import Output
from graphql_auth.schema import UserNode
from graphql_auth.utils import revoke_user_refresh_token
from graphql_jwt.decorators import token_auth, login_required
from graphql_jwt.refresh_token.shortcuts import refresh_token_lazy
from graphql_jwt.shortcuts import get_token

from .models import VerificationCode, User


class VerificationCodeType(DjangoObjectType):
    class Meta:
        model = VerificationCode


class GenerateVerificationCode(Output, graphene.Mutation):
    """
    获取验证码

    参数: \n
    email!: 邮箱地址

    返回值: \n
    success: 操作是否成功 \n
    errors: 如果操作失败，返回失败原因 \n
    """
    class Arguments:
        email = graphene.String(required=True)

    def mutate(self, info, email):
        res, msg = VerificationCode.generate_code(email)
        if not res:
            return GenerateVerificationCode(success=False, errors={"email": msg})
        return GenerateVerificationCode(success=True)


class Register(Output, graphene.Mutation):
    """
    用户注册

    参数: \n
    username!: 用户名 \n
    email!: 邮箱 \n
    password!: 密码 \n
    code!: 验证码 \n

    返回值: \n
    success: 操作是否成功 \n
    errors: 如果操作失败，返回失败原因 \n
    user: 用户节点 \n
    token: JWT token \n

    描述: \n
    注册账号，注册成功会返回JWT token，注册失败会返回失败的原因
    """

    user = graphene.Field(UserNode)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        code = graphene.Int(required=True)

    def mutate(self, info, email, username, password, code):
        with transaction.atomic():
            if User.objects.filter(email=email).exists():
                return Register(success=False, errors={"email": "当前邮箱已经被使用"})
            if User.objects.filter(username=username).exists():
                return Register(success=False, errors={"username": "当前用户名已被使用"})
            verification_code = VerificationCode.objects.filter(email=email).first()
            if verification_code is None or verification_code.code != code:
                return Register(success=False, errors={"code": "验证码错误"})

            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            user.status.verified = True
            user.status.save()

            token = get_token(user, info.context)
            refresh_token = refresh_token_lazy(user)
            return Register(success=True, user=user, token=token, refresh_token=refresh_token)


class Login(mutations.ObtainJSONWebToken):
    """
    用户登录

    参数： \n
    username: 用户名 \n
    email: 邮箱 \n
    password!: 密码 \n

    返回值: \n
    success: 操作是否成功 \n
    errors: 如果操作失败，返回失败原因 \n
    user: 用户节点 \n
    token: JWT token \n

    描述:
    可以使用用户名或者邮箱（两者选其一）来登录网站，登录成功会返回JWT token，登录失败会返回失败的原因
    """


class UpdateUsername(Output, graphene.Mutation):
    """
    修改用户名

    访问条件： \n
    用户已登录 (请求中需要携带JWT token)

    参数： \n
    username!: 新的用户名 \n

    返回值: \n
    success: 操作是否成功 \n
    errors: 如果操作失败，返回失败原因 \n
    token: 新的JWT token
    refreshToken: 新的refresh token

    描述: \n
    传递一个新的用户名来修改当前登录用户的用户名
    """

    token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    @token_auth
    def login(cls, root, info, **kwargs):
        return cls()

    class Arguments:
        username = graphene.String(required=True)

    @login_required
    def mutate(self, info, username):
        with transaction.atomic():
            user = info.context.user
            if user.username == username:
                return UpdateUsername(success=True, errors={"username": "新用户名不能和原用户名相同"})
            if User.objects.filter(username=username).exists():
                return UpdateUsername(success=True, errors={"username": "该用户名已被其他用户使用"})

            revoke_user_refresh_token(user)

            user.username = username
            user.save()

            token = get_token(user, info.context)
            refresh_token = refresh_token_lazy(user)

            return UpdateUsername(success=True, token=token, refresh_token=refresh_token)


class PasswordReset(Output, graphene.Mutation):
    """
    重置密码

    参数： \n
    email: 用户邮箱 \n
    code: 用户邮箱收到的验证码 \n
    password!: 新的密码 \n

    返回值:
    success: 操作是否成功 \n
    errors: 如果操作失败，返回失败原因 \n

    描述: \n
    用户忘记密码时通过绑定的邮箱来重置密码
    """

    class Arguments:
        email = graphene.String(required=True)
        code = graphene.Int(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, code, password):
        with transaction.atomic():
            user = User.objects.filter(email=email).first()
            if user is None:
                return PasswordReset(success=False, errors={"email": "当前邮箱还没有注册"})

            verification_code = VerificationCode.objects.filter(email=email).first()
            if verification_code is None or verification_code.code != code:
                return PasswordReset(success=False, errors={"code": "验证码错误"})

            revoke_user_refresh_token(user)
            user.set_password(password)
            user.save()

            return PasswordReset(success=True)


class PasswordChange(Output, graphene.Mutation):
    """
    修改密码

    访问条件： \n
    用户已登录 (请求中需要携带JWT token) \n

    参数： \n
    oldPassword: 旧密码 \n
    newPassword: 新密码 \n

    返回值: \n
    success: 操作是否成功 \n
    errors: 如果操作失败，返回失败原因 \n
    token: 新的JWT token \n
    refreshToken: 新的refresh token

    描述: \n
    在已知旧密码的情况下修改当前用户的密码
    """
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        old_password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    @login_required
    def mutate(self, info, old_password, new_password):
        with transaction.atomic():
            user = info.context.user
            if not user.check_password(old_password):
                return PasswordChange(success=False, errors={"old_password": "原密码错误"})

            user.set_password(new_password)
            user.save()

            revoke_user_refresh_token(user)
            token = get_token(user, info.context)
            refresh_token = refresh_token_lazy(user)

            return PasswordChange(success=True, token=token, refresh_token=refresh_token)


class AuthMutation(graphene.ObjectType):
    generate_verification_code = GenerateVerificationCode.Field()
    register = Register.Field()
    login = Login.Field()
    update_username = UpdateUsername.Field()
    password_reset = PasswordReset.Field()
    password_change = PasswordChange.Field()
    delete_account = mutations.DeleteAccount.Field()

    refresh_token = mutations.RefreshToken.Field()
