<template>
    <div class="background3">
        <div class="page-panel" :style="{left: (screenWidth-700)/2+'px'}">
            <div style="height:50px">
                <label class="title" style="color:rgb(190,190,190)">FORGOTTEN MEMORIES</label>
            </div>
            <hr class="title" style="color:rgb(190,190,190)"/>
            <div :style="{width:700+'px',height:screenHeight-150+'px'}">
                <vue-scroll :ops="scrollsetting">
                    <div @click="ReadMemory(item)" v-for="(item) in memories" :key="item.id" class="memorytile">
                        <div class="label-div">
                            <label class="label-with-pointer" style="color:rgb(190,190,190)">{{item.title}}</label>
                        </div>
                        <div class="label-div">
                            <label class="label-with-pointer" style="color:rgb(190,190,190">{{item.createTime}}</label>
                        </div>
                    </div>
                    <div style="height:50px"/>
                </vue-scroll>      
            </div>
        </div>
    </div>
</template>

<script>
import GetMyMemory from "../../graphql/MemoryPages/GetMyMemory.graphql"
import ReadMemory from '../../graphql/MemoryPages/ReadMemory.graphql'

export default {
    data() {
        var ops = {
            rail:{
                size:"2px"
            },
            bar:{
                opacity:0.5,
                background:'gray'
            }
        }
        return {
            scrollsetting: ops,
            memories: [],
            screenHeight: document.documentElement.clientHeight,
            screenWidth: document.documentElement.clientWidth
        }
    },
    mounted() {
        this.$apollo.mutate({
            mutation: GetMyMemory,
            variables: {
                name: JSON.parse(localStorage.getItem('user')).name
            }
        }).then(data => {
            console.log(data.data);
            let result = data.data.getAllMemory;
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
                        privacy: result.memorys[i].privacy==0?false:true,
                        activity: result.memorys[i].activity,
                        audio: result.memorys[i].audio,
                        picture: result.memorys[i].picture
                    };
                    result_memories.push(memory);
                }
                result_memories.reverse();
                this.memories = result_memories;
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
        ReadMemory(memory) {
            console.log(memory)
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