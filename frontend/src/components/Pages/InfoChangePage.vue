<template>
    <div class="background2">
        <router-link :to="{ name: 'personal' }">
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
                <el-form :model="changeForm"
                        ref="changeForm" 
                        :rules="changeRules" 
                        label-position="left" 
                        label-width="300px"
                        :hide-required-asterisk="true">
                    <el-form-item prop="username">
                        <i slot="label" class="form-label" style="font-size:24px">NEW USERNAME</i>
                        <el-input style="width:300px" v-model="changeForm.username" :placeholder="name"></el-input>
                    </el-form-item>
                </el-form>
            </div>
            <div style="margin-top:50px;height:40px;text-align:center">
                <el-button class="button-common" style="font-size:24px" @click="submit">RESET</el-button>
            </div>
            <div style="text-align:center;height:20px;">
                <router-link :to="{ name: 'passwordchange' }">
                    <el-button class="button-back" style="font-size:16px">reset password</el-button>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import RefershToken from '../../graphql/RefreshToken.graphql'
import UpdateUsername from '../../graphql/UserInfoPages/InfoChange.graphql'
import validator from '../../utils/validator'
import errorNote from '../../utils/error'


export default {
    inject: ['reload'],
    data() {
        return {
            name: JSON.parse(localStorage.getItem('user'))['name'],
            changeForm: {
                username: ''
            },
            changeRules: {
                username: [
                    {
                        required: true,
                        message: errorNote.emptyUsername,
                        trigger: 'blur'
                    },
                    {
                        validator: validator.username,
                        message: errorNote.incorrectUsername,
                        trigger: ['blur', 'change']
                    }
                ]
            },
            screenWidth: document.documentElement.clientWidth,
            screenHeight: document.documentElement.clientHeight
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
    methods:{
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
                    this.updateusername();
                }
                else {
                    alert(errorNote.validateExpired);
                    localStorage.removeItem('user');
                    localStorage.removeItem('token');
                    localStorage.removeItem('refreshToken');
                    this.$router.push({name:'index'});
                }
            }).catch(error=>{
                console.log(error);
                alert(errorNote.netWorkError);
            });
        },
        updateusername() {
            this.$apollo.mutate({
                mutation: UpdateUsername,
                variables: {
                    username: this.changeForm.username
                },
                client: 'withtoken'
            }).then(data=>{
                if(data.data.updateUsername.success){
                    alert('Updated successfully!');
                    var newuser = JSON.parse(localStorage.getItem('user'));
                    newuser.name = this.changeForm.username;
                    localStorage.setItem('user', JSON.stringify(newuser));
                    localStorage.setItem('token', data.data.updateUsername.token);
                    localStorage.setItem('refreshToken', data.data.updateUsername.refreshToken);
                    this.$router.push({name: 'personal'});
                }
                else{
                    alert(data.data.updateUsername.errors.code);
                }
            }).catch(error=>{
                console.log(error);
                alert(errorNote.netWorkError);
            });
        },
        submit() {
            this.$refs['changeForm'].validate((valid)=>{
                if(!valid){
                    return;
                }
                this.refreshToken();
            });
        }
    }
}
</script>>