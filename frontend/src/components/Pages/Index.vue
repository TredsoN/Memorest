<template>
    <div>
        目前啥都没有的主界面
        <br/>
        <router-link :to="{ name: 'login' }">
            <el-button v-if="!isLogined">登录</el-button>
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

<style scoped>

</style>