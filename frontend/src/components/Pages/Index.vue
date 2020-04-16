<template>
    <div>
        目前啥都没有的主界面
        <br/>
        <router-link :to="{ name: 'login' }">
            <el-button>登录</el-button>
        </router-link>
    </div>
</template>

<script>
    export default {
        name: 'Index'
    }
</script>

<style scoped>

</style>