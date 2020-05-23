<template>
    <div class="background2">
        <router-link :to="{ name: 'infochange' }">
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
                <el-form :model="changePsForm" 
                        ref="changePsForm" 
                        :rules="changePsRules" 
                        label-position="left" 
                        label-width="300px"
                        :hide-required-asterisk="true">
                    <el-form-item prop="oldpswd">
                        <i slot="label" class="form-label" type="password" style="font-size:24px" show-password>ORIGINAL PASSWORD</i>
                        <el-input style="width:300px" v-model="changePsForm.oldpswd" show-password></el-input>
                    </el-form-item>
                    <el-form-item prop="newpswd1">
                        <i slot="label" class="form-label" type="password" style="font-size:24px" show-password>NEW PASSWORD</i>
                        <el-input style="width:300px" v-model="changePsForm.newpswd1" show-password></el-input>
                    </el-form-item>
                    <el-form-item prop="newpswd2">
                        <i slot="label" class="form-label" type="password" style="font-size:24px" show-password>PASSWORD CFM</i>
                        <el-input style="width:300px" v-model="changePsForm.newpswd2" show-password></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <div style="margin-top:50px;height:40px;text-align:center">
                <el-button class="button-common" style="font-size:24px" @click="submit">RESET</el-button>
            </div>
        </div>
    </div>
</template>

<script>
import RefershToken from '../../graphql/RefreshToken.graphql'
import UpdatePassword from '../../graphql/UserInfoPages/PasswordChange.graphql'
import validator from '../../utils/validator'
import errorNote from '../../utils/error'


export default {
    data() {
        const validatePassword = (rule, value, callback) => {
            const reg = validator.regPassword;
            if (!reg.test(value)) {
                callback(new Error());
            }
            if (this.changePsForm.newpswd2 !== '') {
                this.$refs.signUpForm.validateField();
            }
            callback();
        };
        const validateCheckPassword = (rule, value, callback) => {
            if (value !== this.changePsForm.newpswd1) {
                callback(new Error());
            }
            callback();
        };
        return{
            changePsForm: {
                oldpswd: '',
                newpswd1: '',
                newpswd2: ''
            },
            changePsRules:{
                oldpswd:[
                    {
                        required: true,
                        message: errorNote.emptyOldPassword,
                        trigger: 'blur'
                    },
                    {
                        validator: validator.password,
                        message: errorNote.incorrectPassword,
                        trigger: ['blur', 'change']
                    }
                ],
                newpswd1:[
                    {
                        required: true,
                        message: errorNote.emptyNewPassword,
                        trigger: 'blur'
                    },
                    {
                        validator: validatePassword,
                        message: errorNote.incorrectPassword,
                        trigger: ['blur', 'change']
                    }
                ],
                newpswd2:[
                    {
                        required: true,
                        message: errorNote.emptyCheckNewPassword,
                        trigger: 'blur'
                    },
                    {
                        validator: validateCheckPassword,
                        message: errorNote.incorrectCheckNewPassword,
                        trigger: ['blur', 'change']
                    }
                ],
            },
            screenHeight: document.documentElement.clientHeight,
            screenWidth: document.documentElement.clientWidth
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
        refreshToken() {
            this.$apollo.mutate({
                mutation: RefershToken,
                variables: {
                    rtoken: localStorage.getItem('refreshToken')
                },
            }).then(data=>{
                if(data.data.refreshToken.success){
                    localStorage.setItem('token', data.data.refreshToken.token);
                    localStorage.setItem('refreshToken', data.data.refreshToken.refreshToken);
                    this.updatepassword();
                }
                else {
                    alert(errorNote.validateExpired);
                    localStorage.removeItem('user');
                    localStorage.removeItem('token');
                    localStorage.removeItem('refreshToken');
                    this.$router.push({name:'index'});
                }
            }).catch(error=>{
                alert(errorNote.netWorkError);
                console.log(error);
            });
        },
        updatepassword(){
            this.$apollo.mutate({
                mutation: UpdatePassword,
                variables: {
                    np: this.changePsForm.newpswd1,
                    op: this.changePsForm.oldpswd
                },
                client: 'withtoken'
            }).then(data=>{
                if(data.data.passwordChange.success){
                    alert('Updated Successfully!');
                    localStorage.setItem('token', data.data.passwordChange.token);
                    localStorage.setItem('refreshToken', data.data.passwordChange.refreshToken);
                    this.$router.push({name: 'personal'});
                }
                else{
                    alert(data.data.passwordChange.errors.code);
                }
            }).catch(error=>{
                alert(errorNote.netWorkError);
                console.log(error);
            });
        },
        submit() {
            this.$refs['changePsForm'].validate((valid)=>{
                if(!valid){
                    return;
                }
                this.refreshToken();
            });
        }
    }
}
</script>