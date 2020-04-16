<template>
    <div class="background">
        <el-tabs v-model="activeTag">
            <el-tab-pane label="SIGN IN" name="signIn">
                <div class="form-loginandup">
                <el-form :model="signInForm"
                         ref="signInForm"
                         :rules="signInRules"
                         label-width="300px"
                         label-position="left"
                         hide-required-asterisk=true>
                    <el-form-item prop="usernameOrEmail">
                        <i slot="label" class="form-label">USERNAME/EMAIL</i>
                        <el-input v-model="signInForm.usernameOrEmail"></el-input>
                    </el-form-item>
                    <el-form-item prop="password" style="width:700px">
                        <i slot="label" class="form-label">PASSWORD</i>
                        <el-input style="width:300px" type="password" v-model="signInForm.password" show-password></el-input>
                        <router-link :to="{ name: 'passwordfind' }">
                            <el-button class="button-inputside"
                                    style="width:100px"
                                    @click="getCode">
                                forget password?
                            </el-button>
                        </router-link>
                    </el-form-item>
                    <el-button class="button-common" style="margin-top:20px" type="primary" @click="login">START</el-button>
                </el-form>
                </div>
            </el-tab-pane>
            <el-tab-pane label="SIGN UP" name="signUp">
                <div class="form-loginandup">
                <el-form :model="signUpForm"
                         ref="signUpForm"
                         :rules="signUpRules"
                         label-width="300px"
                         label-position="left" 
                         hide-required-asterisk=true>
                    <el-form-item prop="email" style="width:700px">
                        <i slot="label" class="form-label">EMAIL</i>
                        <el-input style="width:300px" v-model="signUpForm.email"></el-input>
                        <el-button id="getCodeBtn"
                                class="button-inputside"
                                style="width:100px"
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
                    <el-button class="button-common" style="margin-top:20px" type="primary" @click="register">START</el-button>
                </el-form>
                </div>
            </el-tab-pane>
        </el-tabs>
        <router-link :to="{ name: 'index' }">
            <el-button class="button-inputside" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>
    </div>
</template>

<script>
    import LoginByUsername from '../../graphql/SignInOrUp/LoginByUsername.graphql'
    import LoginByEmail from '../../graphql/SignInOrUp/LoginByEmail.graphql'
    import GenerateVerificationCode from '../../graphql/SignInOrUp/GenerateVerificationCode.graphql'
    import Register from '../../graphql/SignInOrUp/Register.graphql'


    const waitTime = 60;


    const signInOrUp = {
        name: 'SignInOrUp',
        data() {
            const validateUsernameOrEmail = (rule, value, callback) => {
                const regUsername = /^[^@]{1,16}$/;
                const regEmail = /^[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$/;
                if (!regUsername.test(value) && !regEmail.test(value)) {
                    callback(new Error());
                }
                callback();
            };
            const validateUsername = (rule, value, callback) => {
                const reg = /^[^@]{1,16}$/;
                if (!reg.test(value)) {
                    callback(new Error());
                }
                callback();
            };
            const validatePassword = (rule, value, callback) => {
                const reg = /^([a-z_A-Z0-9-.!@#$%\\^&*)(+={}\][/",'<>~·`?:;|]){8,32}$/;
                if (!reg.test(value)) {
                    callback(new Error());
                }
                if (this.signUpForm.checkPassword !== '') {
                    this.$refs.signUpForm.validateField('checkPassword');
                }
                callback();
            };
            const validateCheckPassword = (rule, value, callback) => {
                if (value !== this.signUpForm.password) {
                    callback(new Error('error checkPassword'));
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
                            message: '请输入用户名或邮箱',
                            trigger: 'blur'
                        },
                        {
                            validator: validateUsernameOrEmail,
                            message: '请输入正确的用户名或邮箱',
                            trigger: ['blur', 'change']
                        }
                    ],
                    password: [
                        {
                            required: true,
                            message: '请输入密码',
                            trigger: 'blur'
                        }
                    ]
                },
                signUpRules: {
                    email: [
                        {
                            required: true,
                            message: 'sdasadadsdas',
                            trigger: 'blur'
                        },
                        {
                            type: 'email',
                            message: '请输入正确的邮箱地址',
                            trigger: ['blur', 'change']
                        }
                    ],
                    username: [
                        {
                            required: true,
                            message: '请输入用户名',
                            trigger: 'blur'
                        },
                        {
                            validator: validateUsername,
                            message: '最多 16 个字符',
                            trigger: ['blur', 'change']
                        }
                    ],
                    password: [
                        {
                            required: true,
                            message: '请输入密码',
                            trigger: 'blur'
                        },
                        {
                            validator: validatePassword,
                            message: '字母 / 数字 / 英文标点，长度 8-32',
                            trigger: ['blur', 'change']
                        }
                    ],
                    checkPassword: [
                        {
                            required: true,
                            message: '请再次输入密码',
                            trigger: 'blur'
                        },
                        {
                            validator: validateCheckPassword,
                            message: '两次输入的密码不一致',
                            trigger: ['blur', 'change']
                        }
                    ],
                    code: [
                        {
                            required: true,
                            message: '请输入验证码',
                            trigger: 'blur'
                        }
                    ]
                }
            };
        },
        computed: {
            getCodeBtnEnabled() {
                return this.signUpForm.count === waitTime;
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
                    console.log(this.signUpForm.email);
                    this.$apollo.mutate({
                        mutation: GenerateVerificationCode,
                        variables: {
                            email: this.signUpForm.email
                        }
                    }).then(data => {
                        let result = data.data.generateVerificationCode;
                        console.log(result);
                        if (!result.success) {
                            alert(result.errors.email);
                        } else {
                            this.setTime();
                        }
                    }).catch(error => {
                        alert(error);
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
                        console.log(result);
                        if (!result.success) {
                            alert(result.errors.code);
                        } else {
                            // TODO: 待测试，设置 token + 界面跳转，邮件服务未知错误
                            localStorage.setItem('token', result.token);
                            localStorage.setItem('refreshtoken', result.refreshToken);
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
                        alert(error);
                    });
                });
            },
            login() {
                this.$refs.signInForm.validate((valid) => {
                    if (!valid) {
                        return;
                    }
                    const regUsername = /^[^@]{1,16}$/;
                    const isUsername = regUsername.test(this.signInForm.usernameOrEmail);
                    this.$apollo.mutate({
                        mutation: isUsername ? LoginByUsername : LoginByEmail,
                        variables: isUsername ? {
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
                                alert('用户名或密码不正确');
                            } else {
                                alert(JSON.stringify(result.errors));
                            }
                        } else {
                            localStorage.setItem('token', result.token);
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
                        alert(error);
                    });
                });
            }
        }
    };

    export default signInOrUp
</script>

<style>
    div.background {
        background:url("../../assets/Images/Image1.jpg");
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        position:fixed;
        background-size:100% 100%;
        overflow: auto;
    }
    div.el-tabs.el-tabs--top {
        top: 50px;
        margin: 0 auto;
        width: 600px;
    }
    div.el-tabs__nav-wrap.is-top {
        top: 50px;
    }
    div.el-tabs__active-bar.is-top{
        background-color: rgb(234,213,15);
    }
    div.el-tabs__item.is-top {
        width: 300px;
        height: 50px;
        font-size: 32px;
        color: rgb(154,132,21);
    }
    div.el-tabs__item.is-top:hover {
        color: rgb(234,213,15);
    }
    div.el-tabs__item.is-top.is-active {
        color: rgb(234,213,15);
    }
    div.el-form-item__error {
        font-size: 16px;
    }
    div.el-tabs__content {
        top: 100px;
    }
</style>