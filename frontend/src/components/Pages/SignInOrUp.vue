<template>
    <div class="background1">
        <router-link :to="{ name: 'index' }">
            <el-button class="button-back" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>
        <el-tabs v-model="activeTag">
            <el-tab-pane label="SIGN IN" name="signIn">
                <el-form :model="signInForm"
                         ref="signInForm"
                         :rules="signInRules"
                         label-width="300px"
                         label-position="left"
                         :hide-required-asterisk="true">
                    <el-form-item prop="usernameOrEmail">
                        <i slot="label" class="form-label">USERNAME/EMAIL</i>
                        <el-input v-model="signInForm.usernameOrEmail"></el-input>
                    </el-form-item>
                    <el-form-item prop="password" style="width:700px">
                        <i slot="label" class="form-label">PASSWORD</i>
                        <el-input style="width:300px" type="password" v-model="signInForm.password"
                                  show-password></el-input>
                        <router-link :to="{ name: 'passwordfind' }">
                            <el-button class="button-inputside" style="width:100px;font-size:16px">
                                forget password?
                            </el-button>
                        </router-link>
                    </el-form-item>
                    <el-button class="button-common" style="margin-top:20px;font-size: 24px;" type="primary"
                               @click="login">START
                    </el-button>
                </el-form>
            </el-tab-pane>
            <el-tab-pane label="SIGN UP" name="signUp">
                <el-form :model="signUpForm"
                         ref="signUpForm"
                         :rules="signUpRules"
                         label-width="300px"
                         label-position="left"
                         :hide-required-asterisk="true">
                    <el-form-item prop="email" style="width:700px">
                        <i slot="label" class="form-label">EMAIL</i>
                        <el-input style="width:300px" v-model="signUpForm.email"></el-input>
                        <el-button id="getCodeBtn"
                                   class="button-inputside"
                                   style="width:100px;font-size:16px"
                                   :type="getCodeBtnEnabled ? 'primary' : 'info'"
                                   :disabled="!getCodeBtnEnabled"
                                   @click="getCode">
                            {{ getCodeBtnEnabled ? 'get code' : 'retry (' + signUpForm.count + 's)'}}
                        </el-button>
                    </el-form-item>
                    <el-form-item prop="code">
                        <i slot="label" class="form-label">CODE</i>
                        <el-input v-model="signUpForm.code"></el-input>
                    </el-form-item>
                    <el-form-item prop="username">
                        <i slot="label" class="form-label">NICKNAME</i>
                        <el-input v-model="signUpForm.username"></el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <i slot="label" class="form-label">PASSWORD</i>
                        <el-input type="password" v-model="signUpForm.password" show-password></el-input>
                    </el-form-item>
                    <el-form-item prop="checkPassword">
                        <i slot="label" class="form-label">PASSWORD CFM</i>
                        <el-input type="password" v-model="signUpForm.checkPassword" show-password></el-input>
                    </el-form-item>
                    <el-button class="button-common" style="margin-top:20px;font-size:24px" type="primary"
                               @click="register">START
                    </el-button>
                </el-form>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
    import LoginByUsername from '../../graphql/SignInOrUp/LoginByUsername.graphql'
    import LoginByEmail from '../../graphql/SignInOrUp/LoginByEmail.graphql'
    import GenerateVerificationCode from '../../graphql/SignInOrUp/GenerateVerificationCode.graphql'
    import Register from '../../graphql/SignInOrUp/Register.graphql'
    import validator from '../../validator'
    import error from '../../error'


    const waitTime = 60;


    const signInOrUp = {
        name: 'SignInOrUp',
        data() {
            const validateSignUpPassword = (rule, value, callback) => {
                const reg = validator.regPassword;
                if (!reg.test(value)) {
                    callback(new Error());
                }
                if (this.signUpForm.checkPassword !== '') {
                    this.$refs.signUpForm.validateField();
                }
                callback();
            };
            const validateSignUpCheckPassword = (rule, value, callback) => {
                if (value !== this.signUpForm.password) {
                    callback(new Error());
                }
                callback();
            };
            return {
                activeTag: 'signIn',
                signInForm: {
                    usernameOrEmail: '',
                    password: ''
                },
                signUpForm: {
                    email: '',
                    username: '',
                    password: '',
                    checkPassword: '',
                    code: '',
                    count: waitTime
                },
                signInRules: {
                    usernameOrEmail: [
                        {
                            required: true,
                            message: error.emptyUsernameOrEmail,
                            trigger: 'blur'
                        },
                        {
                            validator: validator.usernameOrEmail,
                            message: error.incorrectUsernameOrEmail,
                            trigger: ['blur', 'change']
                        }
                    ],
                    password: [
                        {
                            required: true,
                            message: error.emptyPassword,
                            trigger: 'blur'
                        },
                        {
                            validator: validator.password,
                            message: error.incorrectPassword,
                            trigger: ['blur', 'change']
                        }
                    ]
                },
                signUpRules: {
                    email: [
                        {
                            required: true,
                            message: error.emptyEmail,
                            trigger: 'blur'
                        },
                        {
                            type: 'email',
                            message: error.incorrectEmail,
                            trigger: ['blur', 'change']
                        }
                    ],
                    username: [
                        {
                            required: true,
                            message: error.emptyUsername,
                            trigger: 'blur'
                        },
                        {
                            validator: validator.username,
                            message: error.incorrectUsername,
                            trigger: ['blur', 'change']
                        }
                    ],
                    password: [
                        {
                            required: true,
                            message: error.emptyPassword,
                            trigger: 'blur'
                        },
                        {
                            validator: validateSignUpPassword,
                            message: error.incorrectPassword,
                            trigger: ['blur', 'change']
                        }
                    ],
                    checkPassword: [
                        {
                            required: true,
                            message: error.emptyCheckPassword,
                            trigger: 'blur'
                        },
                        {
                            validator: validateSignUpCheckPassword,
                            message: error.incorrectCheckPassword,
                            trigger: ['blur', 'change']
                        }
                    ],
                    code: [
                        {
                            required: true,
                            message: error.emptyCode,
                            trigger: 'blur'
                        },
                        {
                            validator: validator.code,
                            message: error.incorrectCode,
                            trigger: ['blur', 'change']
                        }
                    ]
                }
            };
        },
        computed: {
            getCodeBtnEnabled() {
                return this.signUpForm.count === waitTime;
            },
            isUsername() {
                // true 表示用户名登录，false 表示邮箱登录
                const regUsername = validator.regUsername;
                return regUsername.test(this.signInForm.usernameOrEmail);
            }
        },
        methods: {
            setTime() {
                if (this.signUpForm.count === 0) {
                    this.signUpForm.count = waitTime;
                } else {
                    this.signUpForm.count--;
                    setTimeout(this.setTime, 1000);
                }
            },
            getCode() {
                this.$refs.signUpForm.validateField('email', (message) => {
                    if (message) {
                        // 如果校验成功，message 为 ''
                        return;
                    }
                    this.$apollo.mutate({
                        mutation: GenerateVerificationCode,
                        variables: {
                            email: this.signUpForm.email
                        }
                    }).then(data => {
                        let result = data.data.generateVerificationCode;
                        console.log(result);
                        if (!result.success) {
                            alert(JSON.stringify(result.errors));
                        } else {
                            this.setTime();
                        }
                    }).catch(error => {
                        alert(JSON.stringify(error));
                    });
                });
            },
            register() {
                this.$refs.signUpForm.validate((valid) => {
                    if (!valid) {
                        return;
                    }
                    this.$apollo.mutate({
                        mutation: Register,
                        variables: {
                            email: this.signUpForm.email,
                            username: this.signUpForm.username,
                            password: this.signUpForm.password,
                            code: this.signUpForm.code
                        }
                    }).then(data => {
                        let result = data.data.register;
                        console.log('success');
                        console.log(result);
                        if (!result.success) {
                            if (result.errors.code === error.rIncorrectCode) {
                                alert(error.mIncorrectCode);
                            } else if (result.errors.username === error.rUsernameExist) {
                                alert(error.mUsernameExist);
                            } else if (result.errors.email === error.rEmailExist) {
                                alert(error.mEmailExist);
                            } else {
                                alert(JSON.stringify(result.errors));
                            }
                        } else {
                            localStorage.setItem('token', result.token);
                            localStorage.setItem('refreshToken', result.refreshToken);
                            const user = {
                                name: this.signUpForm.username,
                                email: this.signUpForm.email
                            };
                            localStorage.setItem('user', JSON.stringify(user));
                            this.$router.push({
                                name: 'index'
                            });
                        }
                    }).catch(error => {
                        console.log('error');
                        alert(JSON.stringify(error));
                    });
                });
            },
            login() {
                this.$refs.signInForm.validate((valid) => {
                    if (!valid) {
                        return;
                    }
                    this.$apollo.mutate({
                        mutation: this.isUsername ? LoginByUsername : LoginByEmail,
                        variables: this.isUsername ? {
                            username: this.signInForm.usernameOrEmail,
                            password: this.signInForm.password
                        } : {
                            email: this.signInForm.usernameOrEmail,
                            password: this.signInForm.password
                        }
                    }).then(data => {
                        let result = data.data.login;
                        console.log(result);
                        if (!result.success) {
                            if (result.errors.nonFieldErrors[0].code === 'invalid_credentials') {
                                if (this.isUsername) {
                                    alert(error.mIncorrectUsernameOrPassword);
                                } else {
                                    alert(error.mIncorrectEmailOrPassword)
                                }
                            } else {
                                alert(JSON.stringify(result.errors));
                            }
                        } else {
                            localStorage.setItem('token', result.token);
                            localStorage.setItem('refreshToken', result.refreshToken);
                            const user = {
                                name: result.user.username,
                                email: result.user.email
                            };
                            localStorage.setItem('user', JSON.stringify(user));
                            this.$router.push({
                                name: 'index'
                            });
                        }
                    }).catch(error => {
                        alert(JSON.stringify(error));
                    });
                });
            }
        }
    };

    export default signInOrUp
</script>

<style>
    div.el-tabs.el-tabs--top {
        top: 50px;
        margin: 0 auto;
        width: 600px;
    }

    div.el-tabs__nav-wrap.is-top {
        top: 50px;
    }

    div.el-tabs__content {
        overflow: visible;
    }

    div.el-tabs__active-bar.is-top {
        background-color: rgb(234, 213, 15);
    }

    div.el-tabs__item.is-top {
        width: 300px;
        height: 50px;
        font-size: 32px;
        color: rgb(154, 132, 22);
    }

    div.el-tabs__item.is-top:hover {
        color: rgb(234, 213, 15);
    }

    div.el-tabs__item.is-top.is-active {
        color: rgb(234, 213, 15);
    }

    div.el-tabs__content {
        top: 100px;
    }
</style>