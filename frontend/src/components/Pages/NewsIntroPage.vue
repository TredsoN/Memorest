<template>
    <div class="background5">
        <el-button  @click="$router.back(-1)" class="button-back" style="width:100px;top:5px;left:0;position:absolute">
            BACK
        </el-button>

        <router-link :to="{ name: 'newsindex' }">
            <div class="with-shadow" :style="{top:(screenHeight-300)/2+'px',left:(screenWidth-800)/2+'px'}">
                <div style="position:absolute;width:700px;height:150px;color:rgb(225,225,225);text-align:left;font-size:24px;top:20px;left:50px">
                    <p>阿尔兹海默症就像是在公园散步。</p>
                    <p>只是患上阿尔兹海默症后，我的公园总在变。</p>
                </div>
                <div style="position:absolute;width:700px;height:100px;color:rgb(225,225,225);text-align:left;font-size:18px;top:170px;left:50px">
                    <p>——《选择死亡》</p>
                </div>
                <div style="position:absolute;color:rgb(234,213,15);text-align:left;font-size:18px;bottom:20px;right:50px">
                    <label class="goto-grave-label">了解更多 </label>
                    <font-awesome-icon icon="chevron-right"/>
                </div>
            </div>
        </router-link>
    </div>
</template>

<script>
    import { library } from '@fortawesome/fontawesome-svg-core';
    import { faChevronRight} from '@fortawesome/free-solid-svg-icons';

    library.add(faChevronRight);

    export default {
        data() {
            return{
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
    div.with-shadow {
        position:absolute;
        width:800px;
        height:300px;
        background: rgba(0, 0, 0, 0.6);
        box-shadow: 5px 5px 25px rgba(234,182,15,0.5);
    }
    div.with-shadow:hover {
        cursor: pointer;
        box-shadow: 15px 15px 30px rgb(234,213,15);
    }
</style>