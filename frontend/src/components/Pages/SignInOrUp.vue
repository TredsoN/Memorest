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
                    <el-form-item prop="email" label="邮箱">
                        <el-input v-model="signUpForm.email"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="signUpForm.password" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="checkPassword">
                        <el-input type="password" v-model="signUpForm.checkPassword" show-password></el-input>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
    export default {
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
                    code: ''
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
                    ]
                }
            };
        },
        methods: {}
    }
</script>

<style scoped>

</style>