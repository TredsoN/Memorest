<template>
    <div class="background5">
        <router-link :to="{ name: 'index' }">
            <el-button class="button-back" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>

        <div style="color:rgb(225,225,225)" class="page-panel" :style="{left: (screenWidth-700)/2+'px'}">
            <div style="height:50px">
                <label class="title" style="color:rgb(225,225,225)">NEWS</label>
            </div>
            <hr class="title"/>
            <div :style="{width:700+'px',height:screenHeight-150+'px'}">
                <vue-scroll :ops="scrollsetting">
                    <div>
                        <div v-for="(item) in news" :key="item.title" class="memorytile" @click="ReadNews(item)">
                        <div class="label-div">
                            <label class="label-with-pointer" style="font-size:17px">{{item.title}}</label>
                        </div>
                        <div class="label-div">
                            <label class="label-with-pointer">{{item.time}}</label>
                        </div>
                        </div>
                        <div style="height:50px"/>
                    </div>
                </vue-scroll>
            </div>
        </div>
    </div>
</template>

<script>
    import GetAllNews from "../../graphql/NewsPages/GetAllNews.graphql"

    export default {
        data() {
            var ops = {
                rail:{
                    size:"2px"
                },
                bar:{
                    opacity:0.5,
                    background:'yellow'
                }
            }
            return{
                scrollsetting: ops,
                news: [],
                screenWidth: document.documentElement.clientWidth,
                screenHeight: document.documentElement.clientHeight,
            }
        },
        mounted() {
            this.$apollo.mutate({
                mutation: GetAllNews
            }).then(data => {
                console.log(data);
                let result = data.data.getAllNews;
                if (!result.success) {
                    alert(JSON.stringify(result.errors));
                } else {
                    const result_news = [];
                    for (let i = 0; i < result.news.length; i++) {
                        const news = {
                            title: result.news[i].title,
                            content: result.news[i].content,
                            time: result.news[i].time.substr(0,10),
                        };
                        result_news.push(news);
                    }
                    this.news = result_news.reverse();
                }
            }).catch(error => {
                console.log(error);
            });
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
            ReadNews(news) {
                this.$router.push({name:"newsinfo", params:news});
            }
        }
    }
</script>