<template>
    <div>
        <div class="index" :style="{height:7*screenHeight>5*screenWidth?screenHeight+'px':5*screenWidth/7+'px',width:7*screenHeight>5*screenWidth?7*screenHeight/5+'px':screenWidth+'px'}"></div>
        <div>
            <div
                v-for="(item, index) in memories" 
                class="memory"
                @click="ReadMemory(item)"
                :key="item.id"
                :style="{top:50+positionsRand[index][0]*(screenHeight-320)+'px',left:positionsRand[index][1]*(screenWidth-220)+'px'}">
                <memory-circle 
                    :title="item.title"
                    :subject="item.subject"
                    :opacity="item.activity/100"
                    :display-id="index"/>
            </div>
        </div>
        <router-link v-if="!isLogined" :to="{ name: 'login' }">
            <el-button class="button-common" style="text-align:right;width:200px;top:5px;right:20px;position:absolute;font-size:18px;">LOG IN</el-button>
        </router-link>
        <router-link v-else :to="{ name: 'personal' }">
            <el-button class="button-common" style="text-align:right;width:200px;top:5px;right:20px;position:absolute;font-size:18px;">PERSONAL CENTER</el-button>
        </router-link>
        <div class="goto-grave-box">
            <font-awesome-icon icon="chevron-left"/>
            <label class="goto-grave-label"> MEMORY GRAVE</label>
        </div>
        <div class="create-memory">
            <font-awesome-icon icon="plus-circle" />
        </div>
    </div>
</template>

<script>
    import GetRandomAliveMemory from '../../graphql/Index/GetRandomAliveMemory.graphql';
    import ReadMemory from '../../graphql/MemoryPages/ReadMemory.graphql'
    import { library } from '@fortawesome/fontawesome-svg-core';
    import { faPlusCircle, faChevronLeft } from '@fortawesome/free-solid-svg-icons';
    import MemoryCircle from '../Memory/MemoryCircle'

    library.add(faPlusCircle, faChevronLeft);

    export default {
        name: 'Index',
        components: {
            MemoryCircle
        },
        data() {
            return {
                isLogined: localStorage.getItem('token'),
                memories: [],
                screenWidth: document.documentElement.clientWidth,
                screenHeight: document.documentElement.clientHeight,
                positionsRand:[
                    [0.98,1],[0.31,0.92],[0.68,0.88],[0.75,0.06],[0,0],
                    [0.88,0.45],[0.45,0.32],[0.35,0.75],[0,1],[0.04,0.52],
                    [1,0.23],[0.49,0.16],[0.89,0.65],[0.41,0.55],[1,0.79],
                ]
            }
        },
        mounted() {
            this.$apollo.mutate({
                mutation: GetRandomAliveMemory
            }).then(data => {
                let result = data.data.getRandomAliveMemory;
                console.log(result);
                if (!result.success) {
                    alert(JSON.stringify(result.errors));
                } else {
                    const result_memories = [];
                    for (let i = 0; i < result.memorys.length; i++) {
                        const memory = {
                            id: result.memorys[i].id,
                            subject: result.memorys[i].subjectId+'',
                            creatorUsername: result.memorys[i].creatorUsername,
                            title: result.memorys[i].title,
                            content: result.memorys[i].content,
                            createTime: result.memorys[i].createTime.substr(0,10),
                            visitor: result.memorys[i].visitor,
                            privacy: true,
                            activity: result.memorys[i].activity
                        }
                        result_memories.push(memory)
                    }
                    this.memories = result_memories;
                }
            }).catch(error => {
                alert(JSON.stringify(error));
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
            ReadMemory(memory) {
                this.$apollo.mutate({
                    mutation: ReadMemory,
                    variables: {
                        memoryId: memory.id,
                        isOwner: memory.creatorUsername == JSON.parse(localStorage.getItem('user')).name?true:false
                    },
                }).then(data=>{
                    console.log(data);
                    if(data.data.readOneMemory.success){
                        this.$router.push({name:"memoryinfo", params:memory});
                    }
                }).catch(error=>{
                    console.log(error);
                });
            }
        }
    }
</script>

<style>
    .memory {
        position: fixed;
    }
    .memory:hover {
        cursor:pointer;
        z-index: 999;
    }
    .goto-grave-box {
        width: 200px;
        height: 50px;
        position: fixed;
        left: 20px;
        bottom: 5px;
        text-align: left;
        font-size: 24px;
        color: rgb(234, 182, 15);
     }
    .goto-grave-box:hover {
        cursor: pointer;
        color: rgb(234,213,15);
     }
    .goto-grave-label {
        line-height: 50px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }
    .goto-grave-label:hover {
        cursor: pointer;
    }
    .create-memory {
        height: 70px;
        width: 70px;
        position: fixed;
        right: 20px;
        bottom: 5px;
        font-size: 60px;
        color: rgba(234,182,15,0.6);
        text-align: center;
    }
    .create-memory:hover {
        cursor: pointer;
        color: rgb(234,213,15);
    }
</style>