//个人中心界面
<template>
    <div>
        <button @click="goBack">返回</button>
        <p>昵称：{{user.name}}</p>
        <p>邮箱：{{user.email}}</p>
        <button @click="gotoInfoChange">修改个人信息</button>
    </div>
</template>

<script>
import Vue from 'vue'
export default {
    data() {
        return{
            user: Vue.prototype.$user
        }
    },
    methods: {
        gotoInfoChange() {
            this.$router.push({path:'/infochange'});
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>