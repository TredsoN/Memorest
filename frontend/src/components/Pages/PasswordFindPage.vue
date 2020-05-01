<template>
    <div class="background2">
        <router-link :to="{ name: 'login' }">
            <el-button class="button-back" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>

         <div class="page-panel" :style="{left: (screenWidth-700)/2+'px'}">
            <div style="height:50px">
                <label class="title">RESET INFO</label>
            </div>
            <hr class="title"/>
            <div style="margin-top:50px">
                <el-form :model="emailForm" 
                        ref="emailForm" 
                        :rules="emailRules" 
                        label-position="left" 
                        label-width="300px"
                        :hide-required-asterisk="true">
                    <el-form-item prop="email" style="width:800px">
                        <i slot="label" class="form-label" style="font-size:24px">EMAIL</i>
                        <el-input style="width:300px" v-model="emailForm.email"></el-input>
                        <el-button id="getCodeBtn"
                                class="button-inputside"
                                style="width:100px;font-size:16px"
                                :type="getCodeBtnEnabled ? 'primary' : 'info'"
                                :disabled="!getCodeBtnEnabled"
                                @click="getcode">
                            {{ getCodeBtnEnabled ? 'get code' : 'retry (' + emailForm.count + 's)'}}
                        </el-button>
                    </el-form-item>
                </el-form>

                <el-form :model="pswdForm" 
                        ref="pswdForm" 
                        :rules="pswfRules" 
                        label-position="left" 
                        label-width="300px"
                        :hide-required-asterisk="true">
                    <el-form-item prop="code">
                        <i slot="label" class="form-label" style="font-size:24px">CODE</i>
                        <el-input style="width:300px" v-model="pswdForm.code"></el-input>
                    </el-form-item>
                    <el-form-item prop="pswd1">
                        <i slot="label" class="form-label" type="password" style="font-size:24px" show-password>NEW PASSWORD</i>
                        <el-input style="width:300px" v-model="pswdForm.pswd1"></el-input>
                    </el-form-item>
                    <el-form-item prop="pswd2">
                        <i slot="label" class="form-label" type="password" style="font-size:24px" show-password>PASSWORD CFM</i>
                        <el-input style="width:300px" v-model="pswdForm.pswd2"></el-input>
                    </el-form-item>
                </el-form>

                <div style="margin-top:50px;height:40px;text-align:center">
                    <el-button class="button-common" style="font-size:24px" @click="submit">RESET</el-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import GenerateVerificationCode from '../../graphql/SignInOrUp/GenerateVerificationCode.graphql'
import PasswordReset from '../../graphql/UserInfoPages/PasswordReset.graphql'
import validator from '../../utils/validator'
import error from '../../utils/error'


const waitTime = 60;


export default {
    data() {
        const validatePassword = (rule, value, callback) => {
            const reg = validator.regPassword;
            if (!reg.test(value)) {
                callback(new Error());
            }
            if (this.pswdForm.pswd2 !== '') {
                this.$refs.signUpForm.validateField();
            }
            callback();
        };
        const validateCheckPassword = (rule, value, callback) => {
            if (value !== this.pswdForm.pswd1) {
                callback(new Error());
            }
            callback();
        };
        return{
            emailForm: {
                email: '',
                count: waitTime
            },
            pswdForm: {
                code: '',
                pswd1: '',
                pswd2: ''
            },
            emailRules: {
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
                ]
            },
            pswfRules: {
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
                ],
                pswd1: [
                    {
                        required: true,
                        message: error.emptyPassword,
                        trigger: 'blur'
                    },
                    {
                        validator: validatePassword,
                        message: error.incorrectPassword,
                        trigger: ['blur', 'change']
                    }
                ],
                pswd2: [
                    {
                        required: true,
                        message: error.emptyCheckPassword,
                        trigger: 'blur'
                    },
                    {
                        validator: validateCheckPassword,
                        message: error.incorrectCheckPassword,
                        trigger: ['blur', 'change']
                    }
                ]
            },
            screenHeight: document.documentElement.clientHeight,
            screenWidth: document.documentElement.clientWidth
        }
    },
    computed: {
        getCodeBtnEnabled() {
            return this.emailForm.count == waitTime;
        }
    },
    mounted() {
        window.onresize = () => {
            return (() => {
                window.screenWidth = document.documentElement.clientWidth
                window.screenHeight = document.documentElement.clientHeight
                this.screenHeight = document.documentElement.clientHeight
                this.screenWidth = window.screenWidth
            })()
        }
    },
    methods: {
        setTime() {
            if (this.emailForm.count == 0) {
                this.emailForm.count = waitTime;
            } else {
                this.emailForm.count--;
                setTimeout(this.setTime, 1000);
            }
        },
        getcode() {
            this.$refs['emailForm'].validate((valid)=>{
                if(!valid){
                    return;
                }
                this.$apollo.mutate({
                    mutation: GenerateVerificationCode,
                    variables: {
                        email: this.emailForm.email,
                    },
                }).then(data=>{
                    console.log(data);
                    if(data.data.generateVerificationCode.success){
                        alert('发送成功');
                        this.setTime();
                    }
                    else{
                        alert('发送失败');
                        console.log(data.data.generateVerificationCode);
                    }
                }).catch(error=>{
                    alert(error);
                });
            });
        },
        submit() {
            this.$refs['pswdForm'].validate((valid)=>{
                if(!valid){
                    return;
                }
                this.$refs['emailForm'].validate((valid)=>{
                    if(!valid){
                        return;
                    }
                    this.$apollo.mutate({
                        mutation: PasswordReset,
                        variables: {
                            code: parseInt(this.pswdForm.code),
                            email: this.emailForm.email,
                            pswd: this.pswdForm.pswd1
                        },
                    }).then(data=>{
                        console.log(data);
                        if(data.data.passwordReset.success){
                            alert('修改成功');
                            this.$router.push({name: 'index'});
                        }
                        else{
                            alert(data.data.passwordReset.errors.code);
                        }
                    }).catch(error=>{
                        alert(error);
                    });
                });
            });
        },
    }
}
</script>