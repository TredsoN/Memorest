<template>
    <div id="test">
        <input v-model="username"/>
        <button @click="setGlobal"></button>
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
                name:this.username,
                email:""
            }
            Vue.prototype.$user = user;
            this.$router.push({path:'/Page1'});
        }
    }
}
</script>