<template>
    <div class="index">
        <div v-if="!showMemory" class="goto-grave-box" style="text-align:center;height:80px;width:600px;position:absolute;font-size:28px;" :style="{top:(screenHeight-80)/2+'px',left:(screenWidth-600)/2+'px'}" @click="showMemory = true">
            <label class="goto-grave-label">
                If memory is a can, I hope it never expires.
            </label>
        </div>
        
        <transition name = "fade">
            <div v-if="showMemory">
                <div
                    v-for="(item, index) in memories"
                    class="memory"
                    @click="ReadMemory(item)"
                    :key="item.id"
                    :style="{top:50+positionsRand[index][0]*(screenHeight-320)+'px',left:positionsRand[index][1]*(screenWidth-270)+'px'}">
                    <memory-circle
                        :title="item.title"
                        :subject="item.subject"
                        :opacity="0.5+item.activity/200"
                        :display-id="index"/>
                </div>
            </div>
        </transition>

        <div @click="GotoLogin" v-if="!isLogined" class="goto-grave-box" style="top:5px;left:20px;text-align:left;font-size:18px">
            <label class="goto-grave-label">LOG IN</label>
        </div>
        <div @click="GotoPersonal" v-if="isLogined" class="goto-grave-box" style="top:5px;left:20px;text-align:left;font-size:18px">
            <label class="goto-grave-label">WELCOME, {{username}}</label>
        </div>
        <router-link :to="{ name: 'newsintro' }" target='_blank'>
            <div class="goto-grave-box" style="top:5px;right:20px;text-align:right;font-size:18px">
                <label class="goto-grave-label">ABOUT ALZHEIMER </label>
                <font-awesome-icon icon="comment-dots"/>
            </div>
        </router-link>
        <router-link :to="{ name: 'memorygrave' }">
            <div class="goto-grave-box" style="bottom:5px;left:20px;text-align:left;font-size:24px">
                <font-awesome-icon icon="chevron-left"/>
                <label class="goto-grave-label"> MEMORY GRAVE</label>
            </div>
        </router-link>
        <div class="create-memory" @click="WriteMem">
            <font-awesome-icon icon="plus-circle" />
        </div>
        <div class="refresh-memory" @click="RefreshMem">
            <font-awesome-icon icon="random" />
        </div>
    </div>
</template>

<script>
    import GetRandomAliveMemory from '../../graphql/Index/GetRandomAliveMemory.graphql';
    import ReadMemory from '../../graphql/MemoryPages/ReadMemory.graphql'
    import { library } from '@fortawesome/fontawesome-svg-core';
    import { faPlusCircle, faChevronLeft, faCommentDots, faRandom } from '@fortawesome/free-solid-svg-icons';
    import MemoryCircle from '../Elements/MemoryCircle'
    import errorNote from '../../utils/error'

    library.add(faPlusCircle, faChevronLeft, faCommentDots, faRandom);

    export default {
        inject: ['reload'],
        name: 'Index',
        components: {
            MemoryCircle
        },
        data() {
            return {
                showMemory: false,
                isLogined: localStorage.getItem('token'),
                username: localStorage.getItem('user')? JSON.parse(localStorage.getItem('user')).name : '',
                memories: [],
                screenWidth: document.documentElement.clientWidth,
                screenHeight: document.documentElement.clientHeight,
                positionsRand:[
                    [0.68,0.88],[0.41,0.55],[0.75,0.06],[0,1],[0.35,0.75],
                    [0.88,0.45],[0.31,0.92],[0.98,1],[0.45,0.32],[0.04,0.52],
                    [1,0.23],[0.49,0.16],[0.89,0.65],[0,0],[1,0.79],
                ]
            }
        },
        mounted() {
            this.$apollo.mutate({
                mutation: GetRandomAliveMemory
            }).then(data => {
                let result = data.data.getRandomAliveMemory;
                if (!result.success) {
                    alert(JSON.stringify(result.errors));
                } else {
                    const result_memories = [];
                    for (let i = 0; i < result.memorys.length; i++) {
                        const memory = {
                            id: result.memorys[i].id,
                            subject: result.memorys[i].subjectName,
                            creatorUsername: result.memorys[i].creatorUsername,
                            title: result.memorys[i].title,
                            content: result.memorys[i].content,
                            createTime: result.memorys[i].createTime.substr(0,10),
                            visitor: result.memorys[i].visitor,
                            privacy: true,
                            activity: result.memorys[i].activity,
                            audio: result.memorys[i].audio,
                            picture: result.memorys[i].picture
                        }
                        result_memories.push(memory)
                    }
                    this.memories = result_memories;
                }
            }).catch(error => {
                console.log(error);
                alert(errorNote.netWorkError);
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
                if(!this.isLogined) {
                    var {href} = this.$router.resolve({name:"indexmemoryinfo", query:memory});
                    window.open(href,'_blank')
                    return;
                }
                this.$apollo.mutate({
                    mutation: ReadMemory,
                    variables: {
                        memoryId: memory.id,
                        isOwner: memory.creatorUsername == JSON.parse(localStorage.getItem('user')).name?true:false
                    },
                }).then(data=>{
                    if(data.data.readOneMemory.success){
                        var {href} = this.$router.resolve({name:"indexmemoryinfo", query:memory});
                        window.open(href,'_blank')
                    }
                    else
                        alert(errorNote.netWorkError);
                }).catch(error=>{
                    alert(errorNote.netWorkError);
                    console.log(error);
                });
            },
            GotoPersonal() {
                if(localStorage.getItem('token')){
                    const {href} = this.$router.resolve({ name: 'personal' });
                    window.open(href,'_blank')
                }
                else{
                    const {href} = this.$router.resolve({ name: 'login' });
                    window.open(href,'_blank')
                    this.reload();
                }
            },
            GotoLogin() {
                if(!localStorage.getItem('token')){
                    const {href} = this.$router.resolve({ name: 'login' });
                    window.open(href,'_blank')
                }
                else{
                    const {href} = this.$router.resolve({ name: 'personal' });
                    window.open(href,'_blank');
                    this.reload();
                }
            },
            WriteMem() {
                if(localStorage.getItem('token')){
                    const {href} = this.$router.resolve({ name: 'selectSubject' });
                    window.open(href,'_blank')
                }
                else{
                    const {href} = this.$router.resolve({ name: 'login' });
                    window.open(href,'_blank')
                }
            },
            RefreshMem() {
                this.reload();
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
        z-index: 777;
    }
    .goto-grave-box {
        position: fixed;
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
        position: fixed;
        right: 20px;
        bottom: 20px;
        font-size: 40px;
        color: rgb(234,182,15);
        text-align: center;
    }
    .create-memory:hover {
        cursor: pointer;
        color: rgb(234,213,15);
    }
    .refresh-memory {
        position: fixed;
        right: 80px;
        bottom: 20px;
        font-size: 40px;
        color: rgb(234,182,15);
        text-align: center;
    }
    .refresh-memory:hover {
        cursor: pointer;
        color: rgb(234,213,15);
    }
</style>