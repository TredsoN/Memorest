<template>
    <div class="card">
        <router-link :to="{ name: 'index'}">
            <el-button>返回</el-button>
        </router-link>

        <p>昵称：{{user.name}}</p>
        <p>邮箱：{{user.email}}</p>

        <router-link :to="{ name: 'infochange' }">
            <el-button>修改个人信息</el-button>
        </router-link>

        <router-link :to="{ name: 'index' }">
            <el-button @click="logout">退出登录</el-button>
        </router-link>
    </div>
</template>

<script>
export default {
    data() {
        return{
            user: localStorage.getItem('user')? JSON.parse(localStorage.getItem('user')) : ''
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('user');
            localStorage.removeItem('token');
        }
    }
}
</script>

<style>
    .card {
        background: url('http://106.13.41.151:8087/Assign6.png') center center no-repeat;
    }
</style>