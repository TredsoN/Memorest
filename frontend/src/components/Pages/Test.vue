<template>
    <div id="test">
        <input v-model="username"/>
        <button @click="setGlobal">个人中心</button>
    </div>
</template>

<script>
import Vue from 'vue'
export default {
    name:"Test",
    data() {
        return {
            username: ''
        }
    },
    methods:{
        setGlobal() {
            var user = {
                name: this.username,
                email: "972075430@qq.com"
            }
            Vue.prototype.$user = user;
            this.$router.push({path:'/personal'});
        }
    }
}
</script>