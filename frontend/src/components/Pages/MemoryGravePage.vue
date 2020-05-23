<template>
    <div class="background4">
        <div v-if="!showMemory" class="goto-main-box" style="text-align:center;height:80px;width:800px;position:absolute;font-size:28px;" :style="{top:(screenHeight-80)/2+'px',left:(screenWidth-800)/2+'px'}" @click="showMemory = true">
            <label class="goto-main-label">
                The past is all false, memory is a road without return.
            </label>
        </div>

        <transition name = "fade">
            <div v-if="showMemory">
                <div
                    v-for="(item, index) in memories" 
                    class="memory"
                    :key="item"
                    :style="{top:50+positionsRand[index][0]*(screenHeight-320)+'px',left:positionsRand[index][1]*(screenWidth-220)+'px'}">
                    <memory-circle 
                        :title="item"
                        :display-id="index"/>
                </div>
            </div>
        </transition>
        
        <div @click="GotoLogin" v-if="!isLogined" class="goto-main-box" style="top:5px;left:20px;text-align:left;font-size:18px">
            <label class="goto-main-label">LOG IN</label>
        </div>
        <div @click="GotoPersonal" v-if="isLogined" class="goto-main-box" style="top:5px;left:20px;text-align:left;font-size:18px">
            <label class="goto-main-label">MY FORGOTTEN MEMORIES</label>
        </div>
        <router-link :to="{ name: 'newsintro' }" target="_blank">
            <div class="goto-main-box" style="top:5px;right:20px;text-align:right;font-size:18px">
                <label class="goto-main-label">ABOUT ALZHEIMER </label>
                <font-awesome-icon icon="comment-dots"/>
            </div>
        </router-link>
        <router-link :to="{ name: 'index' }">
            <div class="goto-main-box" style="bottom:5px;right:20px;text-align:right;font-size:24px">
                <label class="goto-main-label">MEMORY FOREST </label>
                <font-awesome-icon icon="chevron-right"/>
            </div>
        </router-link>
    </div>
</template>

<script>
    import GetRandomDeadMemory from '../../graphql/Index/GetRandomDeadMemory.graphql';
    import { library } from '@fortawesome/fontawesome-svg-core';
    import { faPlusCircle, faChevronRight, faCommentDots} from '@fortawesome/free-solid-svg-icons';
    import MemoryCircle from '../Elements/DeadMemoryCircle.vue'
    import errorNote from '../../utils/error'

    library.add(faPlusCircle, faChevronRight, faCommentDots);

    export default {
        components: {
            MemoryCircle
        },
        data() {
            return {
                showMemory: false,
                isLogined: localStorage.getItem('token'),
                memories: [],
                screenWidth: document.documentElement.clientWidth,
                screenHeight: document.documentElement.clientHeight,
                positionsRand:[
                    [0.68,0.88],[0.41,0.55],[0,0],[0.75,0.06],[0,1],
                    [0.88,0.45],[0.31,0.92],[0.49,0.16],[1,0.23],[0.89,0.65],
                ]
            }
        },
        mounted() {
            this.$apollo.mutate({
                mutation: GetRandomDeadMemory
            }).then(data => {
                let result = data.data.getRandomDeadMemory;
                if (!result.success) {
                    alert(JSON.stringify(result.errors));
                } else {
                    for (let i = 0; i < result.memorys.length; i++)
                        this.memories.push(result.memorys[i].title)
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
            GotoPersonal() {
                if(localStorage.getItem('token')){
                    const {href} = this.$router.resolve({ name: 'myforgottenmemories' });
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
                    const {href} = this.$router.resolve({ name: 'myforgottenmemories' });
                    window.open(href,'_blank');
                    this.reload();
                }
            },
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
    .goto-main-box {
        position: fixed;
        color: rgb(190, 190, 190);
     }
    .goto-main-box:hover {
        cursor: pointer;
        color: white;
     }
    .goto-main-label {
        line-height: 50px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }
    .goto-main-label:hover {
        cursor: pointer;
    }
</style>