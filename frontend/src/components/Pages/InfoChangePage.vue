<template>
    <div>
        <button @click="goBack">返回</button>

        <el-form :model="changeForm" ref="changeForm" :rules="changeRules" label-position="right">
            <el-form-item prop="username" label="用户名">
                <el-input v-model="changeForm.username"></el-input>
            </el-form-item>
        </el-form>

        <button @click="submit">确定</button>
        <button @click="gotoPassChange">修改密码</button>
    </div>
</template>

<script>
import gql from 'graphql-tag';

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
        submit() {
            this.$refs['changeForm'].validate((valid)=>{
                if(!valid){
                    return;
                }
                this.$apollo.mutate({
                    mutation: gql`mutation($username: String!){
                        updateUsername(username: $username){
                            success
                            errors
                        }
                    }`,
                    variables: {
                        username: this.changeForm.username
                    },
                    client: 'withtoken'
                }).then(data=>{
                    var result = JSON.parse(JSON.stringify(data));
                    console.log(result.data);
                }).catch(error=>{
                    alert(error);
                });
            });
        },
        gotoPassChange() {
            this.$router.push({path:'/passwordchange'});
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>>