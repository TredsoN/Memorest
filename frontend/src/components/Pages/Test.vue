<template>
    <div id="test">
        <input v-model="username"/>
        <button @click="setGlobal">个人中心</button>
    </div>
</template>

<script>
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
            localStorage.setItem('user', JSON.stringify(user));
            this.$router.push({path:'/personal'});
        }
    }
}
</script>