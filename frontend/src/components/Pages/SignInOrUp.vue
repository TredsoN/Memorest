import gql from "graphql-tag";
<template>
    <div>
        <el-tabs v-model="activeTag">
            <el-tab-pane label="Sign In" name="signIn">
                <el-form :model="signInForm"
                         ref="signInForm"
                         :rules="signInRules"
                         label-position="right">
                    <el-form-item prop="email" label="邮箱">
                        <el-input v-model="signInForm.email"></el-input>
                    </el-form-item>
                    <el-form-item prop="password" label="密码">
                        <el-input type="password" v-model="signInForm.password" show-password></el-input>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
            <el-tab-pane label="Sign Up" name="signUp">
                <el-form :model="signUpForm"
                         ref="signUpForm"
                         :rules="signUpRules"
                         label-position="right">
                    <el-form-item label="邮箱" prop="email" ref="signUpEmail">
                        <el-input v-model="signUpForm.email"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="signUpForm.password" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="checkPassword">
                        <el-input type="password" v-model="signUpForm.checkPassword" show-password></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button id="getCodeBtn"
                                   :type="getCodeBtnEnabled ? 'primary' : 'info'"
                                   :disabled="!getCodeBtnEnabled"
                                   @click="getCode">
                            {{ getCodeBtnEnabled ? '发送验证码' : '重新发送 (' + signUpForm.count + 's)'}}
                        </el-button>
                    </el-form-item>
                    <el-form-item label="验证码" prop="code">
                        <el-input v-model="signUpForm.code"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="register">注册</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
    // import GenerateVerificationCode from '../../graphql/SignInOrUp/GenerateVerificationCode.graphql'
    import gql from 'graphql-tag'


    const waitTime = 60;


    const signInOrUp = {
        name: 'SignInOrUp',
        data() {
            const validatePassword = (rule, value, callback) => {
                const reg = /^([a-z_A-Z0-9-.!@#$%\\^&*)(+={}\][/",'<>~·`?:;|]){8,32}$/;
                if (!reg.test(value)) {
                    callback(new Error('error password'));
                }
                if (this.signUpForm.checkPassword !== '') {
                    this.$refs.signUpForm.validateField('checkPassword');
                }
                callback();
            };
            const validateCheckPassword = (rule, value, callback) => {
                if (value !== this.signUpForm.password) {
                    callback(new Error('error checkPassword'));
                } else {
                    callback();
                }
            };
            return {
                activeTag: 'signIn',
                signInForm: {
                    email: '',
                    password: ''
                },
                signUpForm: {
                    email: '',
                    password: '',
                    checkPassword: '',
                    code: '',
                    count: waitTime
                },
                signInRules: {
                    email: [
                        {
                            required: true,
                            message: '请输入邮箱地址',
                            trigger: 'blur'
                        },
                        {
                            type: 'email',
                            message: '请输入正确的邮箱地址',
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
                            message: '请输入邮箱地址',
                            trigger: 'blur'
                        },
                        {
                            type: 'email',
                            message: '请输入正确的邮箱地址',
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
                        return;
                    }
                    this.setTime();
                    console.log(this.signUpForm.email);
                    this.$apollo.mutate({
                        // mutation: GenerateVerificationCode,
                        mutation: gql`mutation GenerateVerificationCode ($email: String!) {
                            generateVerificationCode (email: $email) {
                                success
                                errors
                            }
                        }`,
                        variables: {
                            email: this.signUpForm.email
                        }
                    }).then(data => {
                        let result = JSON.parse(JSON.stringify(data));
                        console.log(result.data);
                    }).catch(error => {
                        alert(error);
                    });
                });
            },
            register() {
                // this.$refs.signUpForm.validate((valid) => {
                //     if (!valid) {
                //         return;
                //     }
                //     this.$apollo.mutate({
                //         mutation: GenerateVerificationCode,
                //         variables: {
                //             email: this.signUpForm.email
                //         },
                //         client: 'withtoken'
                //     }).then(data => {
                //         let result = JSON.parse(JSON.stringify(data));
                //         console.log(result);
                //     }).catch(error => {
                //         alert(error);
                //     });
                // });
            }
        }
    };


    export default signInOrUp
</script>

<style scoped>

</style>