<template>
    <div>
        <router-link :to="{ name: 'login'}">
            <el-button>返回</el-button>
        </router-link>

        <el-form :model="emailForm" ref="emailForm" :rules="emailRules" label-position="right">
            <el-form-item prop="email" label="邮箱">
                <el-input v-model="emailForm.email"></el-input>
            </el-form-item>
        </el-form>

        <el-button id="getCodeBtn" :type="getCodeBtnEnabled ? 'primary' : 'info'" :disabled="!getCodeBtnEnabled" @click="getcode">
            {{ getCodeBtnEnabled ? '发送验证码' : '重新发送 (' + emailForm.count + 's)'}}
        </el-button>

        <el-form :model="pswdForm" ref="pswdForm" :rules="pswfRules" label-position="right">
            <el-form-item prop="code" label="邮箱验证码" type="number">
                <el-input v-model="pswdForm.code"></el-input>
            </el-form-item>
            <el-form-item prop="pswd1" label="新密码">
                <el-input v-model="pswdForm.pswd1"></el-input>
            </el-form-item>
            <el-form-item prop="pswd2" label="确认新密码">
                <el-input v-model="pswdForm.pswd2"></el-input>
            </el-form-item>
        </el-form>

        <el-button @click="submit">确定</el-button>
    </div>
</template>

<script>
import GenerateVerificationCode from '../../graphql/SignInOrUp/GenerateVerificationCode.graphql'
import PasswordReset from '../../graphql/UserInfoPages/PasswordReset.graphql'

const waitTime = 60;

export default {
    data() {
        var code = (rule, value, callback)=>{
            if(!value){
                return callback(new Error('请输入验证码'));
            }
            if(value.length!=4){
                return callback(new Error('验证码为4位'));
            }
            return callback();
        }
        var newpswd1 = (rule, value, callback) =>{
            if(!value){
                return callback(new Error('新密码不能为空'));
            }
            const reg = /^([a-z_A-Z0-9-.!@#$%\\^&*)(+={}\][/",'<>~·`?:;|]){8,32}$/;
            if (!reg.test(value)) {
                return callback(new Error('密码格式错误（字母/数字/英文标点，长度为8-32）'));
            }
            return callback();
        };
        var newpswd2 = (rule, value, callback) =>{
            if(value !== this.pswdForm.pswd1){
                return callback(new Error('两次输入密码不一致'));
            }
            return callback();
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
                        message: '邮箱不能为空',
                        trigger: 'blur'
                    },
                    {
                        type: 'email',
                        message: '邮箱格式错误',
                        trigger: 'blur'
                    }
                ]
            },
            pswfRules: {
                code: [
                    {
                        validator: code,
                        trigger: 'blur'
                    }
                ],
                pswd1: [
                    {
                        validator: newpswd1,
                        trigger: 'blur'
                    }
                ],
                pswd2: [
                    {
                        validator: newpswd2,
                        trigger: 'blur'
                    }
                ]
            }
        }
    },
    computed: {
        getCodeBtnEnabled() {
            return this.emailForm.count == waitTime;
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
                    }).catch(error=>{
                        alert(error);
                    });
                });
            });
        },
    }
}
</script>