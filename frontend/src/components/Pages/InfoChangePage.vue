<template>
    <div>
        <button @click="goBack">返回</button>
        <input v-model="newname" :placeholder="name"/>
        <label>{{warning}}</label>
        <button @click="submit">确定</button>
        <button @click="gotoPassChange">修改密码</button>
    </div>
</template>

<script>
import Vue from 'vue';
import gql from 'graphql-tag';

export default {
    inject: ['reload'],
    data() {
        return {
            name: Vue.prototype.$user.name,
            newname: '',
            warning: ''
        }
    },
    methods:{
        submit() {
            if(this.newname == ''){
                this.warning = '用户名不能为空';
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
                    username: this.newname
                },
                client: 'withtoken'
            }).then(data=>{
                alert(data);
            }).catch(error=>{
                alert(error);
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