<template>
    <div class="background2">
        <router-link :to="{ name: 'infochange' }">
            <el-button class="button-back" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>

        <div class="page-panel">
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
                        hide-required-asterisk=true>
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

export default {
    data() {
        var oldpswd = (rule, value, callback) =>{
            if(!value){
                return callback(new Error('旧密码不能为空'));
            }
            const reg = /^([a-z_A-Z0-9-.!@#$%\\^&*)(+={}\][/",'<>~·`?:;|]){8,32}$/;
            if (!reg.test(value)) {
                return callback(new Error('密码格式错误（字母/数字/英文标点，长度为8-32）'));
            }
            return callback();
        };
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
            if(value !== this.changePsForm.newpswd1){
                return callback(new Error('两次输入密码不一致'));
            }
            return callback();
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
                        validator: oldpswd,
                        trigger: 'blur'
                    }
                ],
                newpswd1:[
                    {
                        validator: newpswd1,
                        trigger: 'blur'
                    }
                ],
                newpswd2:[
                    {
                        validator: newpswd2,
                        trigger: 'blur'
                    }
                ],
            }
        }
    },
    methods: {
        refreshtoken() {
            this.$apollo.mutate({
                mutation: RefershToken,
                variables: {
                    rtoken: localStorage.getItem('refreshtoken')
                },
            }).then(data=>{
                console.log(data);
                if(data.data.refreshToken.success){
                    localStorage.setItem('token', data.data.refreshToken.token);
                    localStorage.setItem('refreshtoken', data.data.refreshToken.refreshToken);
                }
            }).catch(error=>{
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
                console.log(data);
                if(data.data.passwordChange.success){
                    alert('修改成功');
                    localStorage.setItem('token', data.data.passwordChange.token);
                    localStorage.setItem('refreshtoken', data.data.passwordChange.refreshToken);
                    this.$router.push({name: 'personal'});
                }
                else{
                    alert(data.data.passwordChange.errors.code);
                }
            }).catch(error=>{
                alert(error);
            });
        },
        submit() {
            this.$refs['changePsForm'].validate((valid)=>{
                if(!valid){
                    return;
                }
                this.refreshtoken();
                this.updatepassword();
            });
        }
    }
}
</script>