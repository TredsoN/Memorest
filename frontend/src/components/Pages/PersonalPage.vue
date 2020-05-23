<template>
    <div class="background2">
        <div class="page-panel" :style="{left: (screenWidth-700)/2+'px'}">
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
                <router-link :to="{ name: 'mymemories' }" target="_blank">
                    <el-button class="button-common" style="font-size: 24px">MY MEMORIES</el-button>
                </router-link>
            </div>
            <div style="margin-top:10px;text-align:center">
                <el-button class="button-common" style="font-size: 24px" @click="logout">LOG OUT</el-button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return{
            screenHeight: document.documentElement.clientHeight,
            screenWidth: document.documentElement.clientWidth,
            user: localStorage.getItem('user')? JSON.parse(localStorage.getItem('user')) : ''
        }
    },
    mounted() {
        window.onresize = () => {
            return (() => {
                window.screenWidth = document.documentElement.clientWidth
                window.screenHeight = document.documentElement.clientHeight
                this.screenHeight = document.documentElement.clientHeight
                this.screenWidth = window.screenWidth
            })()
        }
    },
    methods: {
        logout() {
            if(confirm('Confirm to log out?')==true){
                localStorage.removeItem('user');
                localStorage.removeItem('token');
                localStorage.removeItem('refreshToken');
                this.$router.push({name:'index'});
            }
        }
    }
}
</script>

<style>
    div.page-panel {
        position: absolute;
        top: 50px;
        width: 700px;
        text-align:left;
        z-index: 10;
    }
</style>