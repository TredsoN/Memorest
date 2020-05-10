<template>
    <div class="background5">
        <router-link :to="{ name: 'newsindex' }">
            <el-button class="button-back" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>

        <div class="with-shadow2" :style="{width:screenWidth*0.9+'px',height:screenHeight*0.9+'px',top:screenHeight*0.05+20+'px',left:screenWidth*0.05+'px'}">
            <div style="position:absolute;height:50px;color:rgb(225,225,225);text-align:left;font-size:24px;top:20px;left:50px" :style="{width:screenWidth*0.9-100+'px'}">
                <p>{{news.title}}</p>
            </div>
            <hr size="2" color="#999" class="news-hr" :style="{width:screenWidth*0.9-100+'px'}"/>
            <div style="position:absolute;color:rgb(225,225,225);text-align:left;font-size:16px;top:100px;left:50px" :style="{width:screenWidth*0.9-100+'px',height:screenHeight*0.9-120+'px'}">
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
        background: rgba(0, 0, 0, 0.6);
        box-shadow: 5px 5px 25px rgba(234,182,15,0.5);
    }
    hr.news-hr {
        position:absolute;
        top:80px;
        left: 50px;
        filter: alpha(opacity=100,finishopacity=0,style=3);
    }
</style>