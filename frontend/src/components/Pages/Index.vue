<template>
    <div class="index">
        <memory-circle class="memory"
                       :title="titles[0]"
                       size="large"
                       color="light-yellow"
                       :display-id="0"
                       style="top: -50px; left: -50px;" />
        <memory-circle class="memory"
                       :title="titles[1]"
                       size="medium"
                       color="light-blue"
                       :display-id="1"
                       style="top: 180px; left: 150px;" />
        <memory-circle class="memory"
                       :title="titles[2]"
                       size="small"
                       color="dark-yellow"
                       :display-id="2"
                       style="top: 100px; left: 400px;" />
        <memory-circle class="memory"
                       :title="titles[3]"
                       size="large"
                       color="light-yellow"
                       :display-id="3"
                       style="top: 150px; left: 650px;" />
        <memory-circle class="memory"
                       :title="titles[4]"
                       size="medium"
                       color="light-yellow"
                       :display-id="4"
                       style="top: -50px; right: 450px;" />
        <memory-circle class="memory"
                       :title="titles[5]"
                       size="small"
                       color="light-blue"
                       :display-id="5"
                       style="top: 200px; right: 400px;" />
        <memory-circle class="memory"
                       :title="titles[6]"
                       size="medium"
                       color="light-yellow"
                       :display-id="6"
                       style="top: 100px; right: 200px;" />
        <memory-circle class="memory"
                       :title="titles[7]"
                       size="medium"
                       color="light-blue"
                       :display-id="7"
                       style="bottom: 150px; left: -20px;" />
        <memory-circle class="memory"
                       :title="titles[8]"
                       size="small"
                       color="dark-yellow"
                       :display-id="89"
                       style="bottom: 280px; left: 280px;" />
        <memory-circle class="memory"
                       :title="titles[9]"
                       size="large"
                       color="light-blue"
                       :display-id="9"
                       style="bottom: 50px; left: 420px;" />
        <memory-circle class="memory"
                       :title="titles[10]"
                       size="medium"
                       color="light-yellow"
                       :display-id="10"
                       style="bottom: 120px; left: 650px;" />
        <memory-circle class="memory"
                       :title="titles[11]"
                       size="small"
                       color="dark-blue"
                       :display-id="11"
                       style="bottom: 250px; left: 800px;" />
        <memory-circle class="memory"
                       :title="titles[12]"
                       size="large"
                       color="light-yellow"
                       :display-id="12"
                       style="bottom: -30px; right: 280px;" />
        <memory-circle class="memory"
                       :title="titles[13]"
                       size="medium"
                       color="light-blue"
                       :display-id="13"
                       style="bottom: 200px; right: 350px;" />
        <memory-circle class="memory"
                       :title="titles[14]"
                       size="small"
                       color="dark-yellow"
                       :display-id="14"
                       style="bottom: 150px; right: -30px;" />

        <router-link v-if="!isLogined" :to="{ name: 'login' }">
            <el-button class="button-common button" style="font-size: 32px;">登录</el-button>
        </router-link>
        <router-link v-else :to="{ name: 'personal' }">
            <el-button class="button-common button" style="font-size: 32px;">个人中心</el-button>
        </router-link>
        <div class="goto-grave-box">
            <font-awesome-icon icon="chevron-left" />
            <label class="goto-grave-label">Goto Grave</label>
        </div>
        <font-awesome-icon class="create-memory" icon="plus-circle" />
    </div>
</template>

<script>
    import { library } from '@fortawesome/fontawesome-svg-core';
    import { faPlusCircle, faChevronLeft } from '@fortawesome/free-solid-svg-icons';
    import MemoryCircle from '../Memory/MemoryCircle'
    import GetRandomAliveMemory from '../../graphql/Index/GetRandomAliveMemory.graphql';

    library.add(faPlusCircle, faChevronLeft);

    export default {
        name: 'Index',
        components: {
            MemoryCircle
        },
        data() {
            return {
                isLogined: localStorage.getItem('token'),
                titles: null
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
                    const titles = [];
                    for (let i = 0; i < result.memorys.length; i++) {
                        titles.push(result.memorys[i].title)
                    }
                    this.titles = titles;
                }
            }).catch(error => {
                alert(JSON.stringify(error));
            });
        }
    }
</script>

<style>
    .index {
        background: url('../../assets/Images/index.jpg');
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        position: fixed;
        background-size: 100% 100%;
        overflow: auto;
    }
    .button {
        position: fixed;
        right: 30px;
        top: 30px;
    }
    .memory {
        position: fixed;
    }
    .goto-grave-box {
        position: fixed;
        left: 50px;
        bottom: 50px;
        font-size: xx-large;
        color: white;
     }
    .goto-grave-label {
        margin-left: 20px;
    }
    .create-memory {
        position: fixed;
        right: 50px;
        bottom: 50px;
        font-size: xxx-large;
        color: rgb(234, 182, 15);
    }
</style>