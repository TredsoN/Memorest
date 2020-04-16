<template>
    <div>
        目前啥都没有的主界面
        <br/>
        <router-link :to="{ name: 'login' }">
            <button class="button" v-if="!isLogined">登录</button>
        </router-link>
        
        <router-link :to="{ name: 'personal' }">
            <el-button v-if="isLogined">个人中心</el-button>
        </router-link>
    </div>
</template>

<script>
    export default {
        name: 'Index',
        data() {
            return {
                isLogined: localStorage.getItem('token'),
            }
        }
    }
</script>

<style>

</style>