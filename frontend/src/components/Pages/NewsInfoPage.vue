<template>
    <div class="background5">
        <router-link :to="{ name: 'newsindex' }">
            <el-button class="button-back" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>

        <div class="with-shadow2" :style="{top:(screenHeight-600)/2+'px',left:(screenWidth-1200)/2+'px'}">
            <div style="position:absolute;width:1100px;height:50px;color:rgb(225,225,225);text-align:left;font-size:24px;top:20px;left:50px">
                <p>{{news.title}}</p>
            </div>
            <hr size="2" color="#999" class="news-hr"/>
            <div style="position:absolute;width:1100px;height:480px;color:rgb(225,225,225);text-align:left;font-size:16px;top:100px;left:50px">
                <vue-scroll :ops="scrollsetting">  
                    <div v-html="news.content"/>
                </vue-scroll>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            var ops = {
                rail:{
                    size:"6px"
                },
                bar:{
                    keepShow:true,
                    opacity:0.5,
                    background:'yellow'
                }
            }
            return{
                scrollsetting: ops,
                news:this.$route.params,
                screenWidth: document.documentElement.clientWidth,
                screenHeight: document.documentElement.clientHeight,
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
        }
    }
</script>


<style>
    div.with-shadow2 {
        position:absolute;
        width:1200px;
        height:600px;
        background: rgba(0, 0, 0, 0.6);
        box-shadow: 5px 5px 25px rgba(234,182,15,0.5);
    }
    hr.news-hr {
        position:absolute;
        width:1100px;
        top:80px;
        left: 50px;
        filter: alpha(opacity=100,finishopacity=0,style=3);
    }
</style>