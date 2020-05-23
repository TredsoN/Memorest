<template>
    <div class="index">
        <router-link to>
            <el-button @click="$router.back(-1)" class="button-back" style="width:100px;top:5px;left:0;position:absolute">
                BACK
            </el-button>
        </router-link>

        <svg :width="screenHeight*0.9" :height="screenHeight*0.9" style="position:absolute" :style="{left:(screenWidth-screenHeight*0.9)/2,top:screenHeight*0.05}">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" stop-color="#000000"/>
                        <stop offset="90%" stop-color="#000000"/>
                        <stop offset="91%" :stop-color="outterColor"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle :cx="screenHeight*0.45" :cy="screenHeight*0.45" :r="screenHeight*0.45" :fill="radialGradient" />
                </mask>
            </defs>
            <rect width="100%" height="100%" :fill="outterColor" :mask="mask" />
        </svg>

        <div style="position:absolute" :style="{width:screenHeight*0.4+'px',height:screenHeight*0.1+'px',left:(screenWidth-screenHeight*0.4)/2+'px',top:screenHeight*0.15+'px'}">
            <label class="content-title" style="word-break:break-all;font-size:28px;line-height:30px" :style="{color:outterColor}">{{memory.title}}</label>
        </div>
        <div style="position:absolute;text-align:left" :style="{width:screenHeight*0.6+'px',height:screenHeight*0.48+'px',left:(screenWidth-screenHeight*0.6)/2+'px',top:screenHeight*0.24+'px'}">
            <vue-scroll :ops="scrollsetting"> 
                <div v-if="memory.subject!=''">
                    <label class="content-title" style="word-break:break-all;line-height:30px;font-size:18px" :style="{color:outterColor}">#{{memory.subject}}</label>
                    <br><br>
                </div>
                <div v-if="memory.audio">
                    <aplayer :music="{
                        title:'记忆留声',
                        artist:memory.creatorUsername,
                        src:'http://106.13.41.151/media/music/' + audio,
                        pic:'http://106.13.41.151:8087/Memorest.jpg',
                        theme:'rgb(234,213,15)'}"/>
                    <br>
                </div>
                <div v-if="memory.picture">
                    <img :width="screenHeight * 0.5"
                         :src="'http://106.13.41.151/media/image/' + picture"
                         alt=""/>
                    <br><br>
                </div>
                <label class="content-title" style="word-break:break-all;line-height:30px;font-size:20px" :style="{color:outterColor}">{{memory.content}}</label>
                <div style="height:50px"/>
            </vue-scroll>
        </div>
        <div style="position:absolute;text-align:right;overflow:visible" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.4)/2+'px',top:screenHeight*0.73+'px'}">
            <label class="content-title" style="line-height:30px;font-size:18px" :style="{color:outterColor}">{{memory.creatorUsername}} {{memory.createTime}}</label>
        </div>
        <div style="position:absolute;text-align:right;overflow:visible" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.5)/2+'px',top:screenHeight*0.78+'px'}">
            <label class="content-title" style="line-height:30px;font-size:18px" :style="{color:outterColor}">visitor {{memory.visitor}}</label>
        </div>
        <div v-if="isMine" style="position:absolute;text-align:left" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.5)/2+'px',top:screenHeight*0.78+'px'}">
            <font-awesome-icon :icon="['far','trash-alt']" style="font-size:22px;color:red"></font-awesome-icon>
            <label class="text-button" @click="DeleteMemory" style="line-height:30px;font-size:22px;color:red"> delete</label>
        </div>
        <div v-if="isMine" style="position:absolute;text-align:left" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.6)/2+'px',top:screenHeight*0.73+'px'}">
            <font-awesome-icon :icon="memory.privacy?['far','eye-slash']:['far','eye']" style="font-size:22px" :style="{color:memory.privacy?'rgb(210,210,210)':outterColor}"></font-awesome-icon>
            <label class="text-button" @click="SetPrivate" style="line-height:30px;font-size:22px" :style="{color:memory.privacy?'rgb(210,210,210)':outterColor}">{{memory.privacy?" set private":" set public"}}</label>
        </div>
    </div>
</template>

<script>
import SetMemoryPrivacy from '../../graphql/MemoryPages/SetPrivacy.graphql'
import DeleteMemory from '../../graphql/MemoryPages/DeleteMemory.graphql'
import { library } from '@fortawesome/fontawesome-svg-core';
import { faTrashAlt } from '@fortawesome/free-regular-svg-icons';
import { faEye } from '@fortawesome/free-regular-svg-icons';
import { faEyeSlash } from '@fortawesome/free-regular-svg-icons';
import aplayer from 'vue-aplayer'

library.add(faTrashAlt, faEye, faEyeSlash);

export default {
    components:{
        aplayer
    },
    data() {
        var ops = {
            rail:{
                size:"2px"
                },
            bar:{
                opacity:0.5,
                background:this.$route.params.subject == ""?'#ffff00':'#00aaff'
            }
        }
        return {
            scrollsetting: ops,
            memory: this.$route.params,
            screenHeight: document.documentElement.clientHeight,
            screenWidth: document.documentElement.clientWidth
        }
    },
    computed: {
        picture() {
            const pictures = this.memory.picture.split(',');
            return pictures[pictures.length - 2];
        },
        audio() {
            const audios = this.memory.audio.split(',');
            return audios[audios.length - 2];
        },
        outterColor() {
            if(this.memory.subject == "")
                return '#ffff00';
            return '#00aaff';
        },
        isMine() {
            if(!localStorage.getItem('token'))
                return false;
            if(JSON.parse(localStorage.getItem('user')).name == this.memory.creatorUsername)
                return true;
            return false;
        },
        radialGradientId() {
            return `radial-gradient-${this.displayId}`
        },
        radialGradient() {
            return `url(#${this.radialGradientId})`
        },
        maskId() {
            return `mask-${this.displayId}`
        },
        mask() {
            return `url(#${this.maskId})`
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
        SetPrivate() {
            this.$apollo.mutate({
                mutation: SetMemoryPrivacy,
                variables: {
                    memoryId: this.memory.id,
                    privacy: this.memory.privacy?0:1
                },
            }).then(data=>{
                if(data.data.setMemoryDensity.success){
                    this.memory.privacy = !this.memory.privacy;
                }
            }).catch(error=>{
                console.log(error);
            });
        },
        DeleteMemory() {
            if(confirm('Confirm to delete?')==true){
                this.$apollo.mutate({
                    mutation: DeleteMemory,
                    variables: {
                        memoryId: this.memory.id,
                    },
                }).then(data=>{
                    if(data.data.deleteMemory.success){
                        this.$router.go(-1)
                    }
                }).catch(error=>{
                    console.log(error);
                });
            }
        }
    }
}
</script>