<template>
    <div>
        <router-link :to="{ name: 'personal'}">
            <el-button>返回</el-button>
        </router-link>

        <el-form :model="changeForm" ref="changeForm" :rules="changeRules" label-position="right">
            <el-form-item prop="username" label="用户名">
                <el-input v-model="changeForm.username"></el-input>
            </el-form-item>
        </el-form>

        <el-button @click="submit">确定</el-button>

        <router-link :to="{ name: 'passwordchange' }">
            <el-button>修改密码</el-button>
        </router-link>
    </div>
</template>

<script>
import RefershToken from '../../graphql/RefreshToken.graphql'
import UpdateUsername from '../../graphql/UserInfoPages/InfoChange.graphql'

export default {
    inject: ['reload'],
    data() {
        var name = (rule, value, callback) =>{
            if(!value){
                return callback(new Error('用户名不能为空'));
            }
            if(value.length > 16){
                return callback(new Error('用户名不能超过16个字符'));
            }
            return callback();
        };
        return {
            name: JSON.parse(localStorage.getItem('user'))['name'],
            changeForm: {
                username: ''
            },
            changeRules: {
                username: [
                    {
                        validator: name,
                        trigger: 'blur'
                    }
                ]
            }
        }
    },
    methods:{
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
        updateusername() {
            this.$apollo.mutate({
                mutation: UpdateUsername,
                variables: {
                    username: this.changeForm.username
                },
                client: 'withtoken'
            }).then(data=>{
                console.log(data);
                if(data.data.updateUsername.success){
                    alert('修改成功');
                    var newuser = JSON.parse(localStorage.getItem('user'));
                    newuser.name = this.changeForm.username;
                    localStorage.setItem('user', JSON.stringify(newuser));
                    localStorage.setItem('token', data.data.updateUsername.token);
                    localStorage.setItem('refreshtoken', data.data.updateUsername.refreshToken);
                    this.$router.push({name: 'personal'});
                }
            }).catch(error=>{
                console.log(error);
            });
        },
        submit() {
            this.$refs['changeForm'].validate((valid)=>{
                if(!valid){
                    return;
                }
                this.refreshtoken();
                this.updateusername();
            });
        }
    }
}
</script>>