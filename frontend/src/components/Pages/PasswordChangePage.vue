<template>
    <div>
        <button @click="goBack">返回</button>
        <input v-model="oldpassword" placeholder="输入原密码"/>
        <label>{{warning1}}</label>
        <input v-model="newpassword1" placeholder="输入新密码"/>
        <label>{{warning2}}</label>
        <input v-model="newpassword2" placeholder="再次输入新密码"/>
        <label>{{warning3}}</label>
        <button @click="submit">确定</button>
    </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
    data() {
        return{
            oldpassword: '',
            newpassword1: '',
            newpassword2: '',
            warning1: '',
            warning2: '',
            warning3: ''
        }
    },
    methods: {
        submit() {
            if(this.oldpassword == ''){
                this.warning1 = '原密码不能为空';
                return;
            }
            if(this.newpassword1 == ''){
                this.warning2 = '新密码不能为空';
                return;
            }
            if(this.newpassword2 == ''){
                this.warning3 = '请再次输入新密码';
                return;
            }
            if(this.newpassword2 != this.newpassword1)
            {
                this.warning3 = '两次输入密码不一致';
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
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>