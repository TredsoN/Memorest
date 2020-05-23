<template>
    <div class="background5">
        <router-link :to="{ name: 'newsindex' }">
            <div class="with-shadow" :style="{top:(screenHeight-300)/2+'px',left:(screenWidth-800)/2+'px'}">
                <div style="position:absolute;width:700px;height:150px;color:rgb(225,225,225);text-align:left;font-size:24px;top:20px;left:50px">
                    <p>Alzheimer's is like walking in a park.</p>
                    <p>It's just that after Alzheimer's, my park is always changing.</p>
                </div>
                <div style="position:absolute;width:700px;height:100px;color:rgb(225,225,225);text-align:left;font-size:18px;top:170px;left:50px">
                    <p>—— Terry Pratchett：Choosing to Die</p>
                </div>
                <div style="position:absolute;color:rgb(234,213,15);text-align:left;font-size:18px;bottom:20px;right:50px">
                    <label class="goto-grave-label">Learn More </label>
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
        box-shadow: 10px 10px 30px rgb(234,213,15);
    }
</style>