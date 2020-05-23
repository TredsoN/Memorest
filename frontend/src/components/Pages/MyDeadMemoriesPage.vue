<template>
    <div class="background3">
        <div class="page-panel" :style="{left: (screenWidth-700)/2+'px'}">
            <div style="height:50px">
                <label class="title" style="color:rgb(190,190,190)">FORGOTTEN MEMORIES</label>
            </div>
            <hr class="titledead"/>
            <div :style="{width:700+'px',height:screenHeight-150+'px'}">
                <vue-scroll :ops="scrollsetting">
                    <div v-for="(item) in memories" :key="item.id" class="deadmemorytile">
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
import GetMyMemory from "../../graphql/MemoryPages/GetMyMemoryDead.graphql"

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
            let result = data.data.getAllMemory;
            if (!result.success) {
                alert(JSON.stringify(result.errors));
            } else {
                const result_memories = [];
                for (let i = 0; i < result.memorys.length; i++) {
                    const memory = {
                        title: result.memorys[i].title,
                        createTime: result.memorys[i].createTime.substr(0,10),
                    };
                    result_memories.push(memory);
                }
                result_memories.reverse();
                this.memories = result_memories;
            }
        }).catch(error => {
            alert('The network is not in good condition. Please try again later.');
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

    }
}
</script>