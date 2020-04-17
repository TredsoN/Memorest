<template>
    <div class="background2">
        <router-link :to="{ name: 'index' }">
            <el-button class="button-back" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>

        <div class="page-panel">
            <div style="height:50px">
                <label class="title">MY</label>
            </div>
            <hr class="title"/>
            <div style="margin-top:50px;height:50px">    
                <div style="float:left;width:300px"><label class="content-title">NICKNAME</label></div>
                <div style="float:left;width:350px"><label class="content-info">{{user.name}}</label></div>
                <router-link :to="{ name: 'infochange' }">
                    <el-button class="button-inputside" icon="el-icon-edit" style="float:left;height:50px;width:50px;font-size:28px">
                    </el-button>
                </router-link>
            </div>
            <div style="margin-top:20px;height:50px">
                <div style="float:left;width:300px"><label class="content-title">EMAIL</label></div>
                <div style="float:left"><label class="content-info">{{user.email}}</label></div>
            </div>
            <div style="margin-top:50px;text-align:center">
                <router-link :to="{ name: 'index' }">
                    <el-button class="button-common" style="font-size: 24px" @click="logout">LOG OUT</el-button>
                </router-link>
            </div>
        </div>
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
    div.page-panel {
        margin: 0 auto;
        margin-top: 50px;
        width: 700px;
        text-align:left;
    }
</style>