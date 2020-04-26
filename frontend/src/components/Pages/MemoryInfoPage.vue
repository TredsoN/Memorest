<template>
    <div>
        <div class="index" :style="{height:7*screenHeight>5*screenWidth?screenHeight+'px':5*screenWidth/7+'px',width:7*screenHeight>5*screenWidth?7*screenHeight/5+'px':screenWidth+'px'}"></div>

        <el-button @click="$router.back(-1)" class="button-back" style="width:100px;top:5px;left:0;position:absolute">
            BACK
        </el-button>

        <svg :width="screenHeight*0.9" :height="screenHeight*0.9" style="position:absolute" :style="{left:(screenWidth-screenHeight*0.9)/2,top:screenHeight*0.05}">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" :stop-color="innerColor"/>
                        <stop offset="90%" :stop-color="innerColor"/>
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
            <label class="content-title" style="word-break:break-all;font-size:36px;line-height:30px" :style="{color:outterColor}">{{memory.title}}</label>
        </div>
        <div v-if="isMine" style="position:absolute;text-align:left" :style="{width:screenHeight*0.55+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.55)/2+'px',top:screenHeight*0.25+'px'}">
            <font-awesome-icon :icon="memory.privacy?['far','eye-slash']:['far','eye']" style="font-size:22px" :style="{color:memory.privacy?'gray':outterColor}"></font-awesome-icon>
            <label class="text-button" @click="SetPrivate" style="line-height:30px;font-size:22px" :style="{color:memory.privacy?'gray':outterColor}">{{memory.privacy?" set private":" set public"}}</label>
        </div>
        <div style="position:absolute;text-align:left;overflow:auto" :style="{width:screenHeight*0.55+'px',height:screenHeight*0.4+'px',left:(screenWidth-screenHeight*0.55)/2+'px',top:screenHeight*0.32+'px'}">
            <label class="content-title" style="word-break:break-all;line-height:30px" :style="{color:outterColor}">{{memory.content}}</label>
        </div>
        <div style="position:absolute;text-align:right;overflow:visible" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.5)/2+'px',top:screenHeight*0.72+'px'}">
            <label class="content-title" style="line-height:30px;font-size:18px" :style="{color:outterColor}">{{memory.creatorUsername}} {{memory.createTime}}</label>
        </div>
        <div v-if="isMine" style="position:absolute;text-align:left" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.5)/2+'px',top:screenHeight*0.72+'px'}">
            <font-awesome-icon :icon="['far','trash-alt']" style="font-size:22px;color:red"></font-awesome-icon>
            <label class="text-button" @click="DeleteMemory" style="line-height:30px;font-size:22px;color:red"> delete</label>
        </div>
        <div style="position:absolute;text-align:right;overflow:visible" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.5)/2+'px',top:screenHeight*0.77+'px'}">
            <label class="content-title" style="line-height:30px;font-size:18px" :style="{color:outterColor}">visitor {{memory.visitor}}</label>
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

library.add(faTrashAlt, faEye, faEyeSlash);

export default {
    data() {
        return {
            memory: this.$route.params,
            screenHeight: document.documentElement.clientHeight,
            screenWidth: document.documentElement.clientWidth
        }
    },
    computed: {
        innerColor() {
            if(this.$route.params.subject == "null")
                return 'rgba(255, 255, 0, 0.12)';
            return 'rgba(0, 170, 255, 0.12)';
        },
        outterColor() {
            if(this.$route.params.subject == "null")
                return '#ffff00';
            return '#00aaff';
        },
        isMine() {
            if(JSON.parse(localStorage.getItem('user')).name == this.$route.params.creatorUsername)
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
                console.log(data);
                if(data.data.setMemoryDensity.success){
                    this.memory.privacy = !this.memory.privacy;
                }
            }).catch(error=>{
                console.log(error);
            });
        },
        DeleteMemory() {
            this.$apollo.mutate({
                mutation: DeleteMemory,
                variables: {
                    memoryId: this.memory.id,
                },
            }).then(data=>{
                console.log(data);
                if(data.data.DeleteMemory.success){
                    this.memory.privacy = !this.memory.privacy;
                }
            }).catch(error=>{
                console.log(error);
            });
        }
    }
}
</script>