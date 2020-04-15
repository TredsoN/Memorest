<template>
    <div>
        <button @click="goBack">返回</button>

        <el-form :model="changePsForm" ref="changePsForm" :rules="changePsRules" label-position="right">
            <el-form-item prop="oldpswd" label="旧密码">
                <el-input v-model="changePsForm.oldpswd" show-password></el-input>
            </el-form-item>
            <el-form-item prop="newpswd1" label="新密码">
                <el-input v-model="changePsForm.newpswd1" show-password></el-input>
            </el-form-item>
            <el-form-item prop="newpswd2" label="再次输入新密码">
                <el-input v-model="changePsForm.newpswd2" show-password></el-input>
            </el-form-item>
        </el-form>
        <button @click="submit">确定</button>
    </div>
</template>

<script>
import gql from 'graphql-tag';

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
            if(value ){
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
        submit() {
            this.$refs['changePsForm'].validate((valid)=>{
                if(!valid){
                    return;
                }
                this.$apollo.mutate({
                    mutation: gql`mutation($op: String!, $np: String!){
                        passwordChange(newPassword: $np, oldPassword: $op){
                            success
                            errors
                            token
                        }
                    }`,
                    variables: {
                        np: this.newpassword1,
                        op: this.oldpassword
                    },
                    client: 'withtoken'
                }).then(data=>{
                    alert(data);
                }).catch(error=>{
                    alert(error);
                });
            });
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>