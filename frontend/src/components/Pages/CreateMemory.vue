<template>
    <div class="create-memory">
        <el-button @click="back" class="button-back" style="width: 100px; top: 5px; left: 0; position: absolute;">
            BACK
        </el-button>
        <div v-if="!isLogined" class="circle">
            <label>{{ loginBeforeCreateMemory }}</label><br/>
            <router-link :to="{ name: 'login' }">
                <el-button class="button-common" style="font-size: 24px;">LOGIN</el-button>
            </router-link>
        </div>
        <div v-else>
            <memory-circle class="circle"
                           color="light-yellow"
                           size="x-large"/>
            <div class="circle form">
                <font-awesome-icon class="close" icon="times"/>
                <el-form :hide-required-asterisk="true"
                         :model="createMemoryForm"
                         :rules="createMemoryRules"
                         ref="createMemoryForm">
                    <el-form-item prop="title" class="memory-title">
                        <el-input v-model="createMemoryForm.title" style="height: 150px;"></el-input>
                    </el-form-item>
                    <el-input
                            v-model="createMemoryForm.content"
                            rows="10"
                            type="textarea"
                            class="memory-content"
                            style= "background-color: transparent;"></el-input>
                    <el-checkbox v-model="createMemoryForm.isPublic" class="public">PUBLIC</el-checkbox>
                    <el-button @click="submit"
                               class="button-common create"
                               type="primary"
                               style="font-size: 24px">
                        <font-awesome-icon icon="paper-plane"/>
                        CREATE
                    </el-button>
                </el-form>
            </div>
            <font-awesome-icon class="add" icon="plus-circle"/>
        </div>
    </div>
</template>

<script>
    import {library} from '@fortawesome/fontawesome-svg-core';
    import {faChevronLeft, faPlusCircle, faTimes, faPaperPlane} from '@fortawesome/free-solid-svg-icons';
    import MemoryCircle from '../Memory/MemoryCircle';
    import CreateMemory from '../../graphql/CreateMemory/CreateMemory.graphql';
    import error from '../../error'
    import RefershToken from "../../graphql/RefreshToken.graphql";

    library.add(faPlusCircle, faChevronLeft, faTimes, faPaperPlane);

    export default {
        name: 'CreateMemory',
        components: {MemoryCircle},
        data() {
            return {
                isLogined: localStorage.getItem('token'),
                loginBeforeCreateMemory: error.loginBeforeCreateMemory,
                createMemoryForm: {
                    title: '',
                    content: '',
                    isPublic: false,
                    picture: '',
                    audio: ''
                },
                createMemoryRules: {}
            }
        },
        methods: {
            back() {
                this.$router.go(-1);
            },
            submit() {
                this.refreshToken();
                this.createMemory();
            },
            refreshToken() {
                this.$apollo.mutate({
                    mutation: RefershToken,
                    variables: {
                        rtoken: localStorage.getItem('refreshToken')
                    }
                }).then(data=>{
                    console.log(data.data);
                    if(data.data.refreshToken.success){
                        localStorage.setItem('token', data.data.refreshToken.token);
                        localStorage.setItem('refreshToken', data.data.refreshToken.refreshToken);
                    }
                }).catch(error=>{
                    console.log(error);
                });
            },
            createMemory() {
                this.$apollo.mutate({
                    mutation: CreateMemory,
                    variables: {
                        memoryData: {
                            creatorUsername: JSON.parse(localStorage.getItem('user')).name,
                            title: this.createMemoryForm.title,
                            content: this.createMemoryForm.content,
                            privacy: this.createMemoryForm.isPublic ? 1 : 0,
                            picture: '',
                            audio: ''
                        }
                    },
                    client: 'withtoken'
                }).then(data => {
                    let result = data.data.createMemory;
                    console.log(result);
                    if (!result.success) {
                        alert(JSON.stringify(result.errors));
                    } else {
                        alert('发布成功');  // TODO: 跳转到个人记忆
                    }
                }).catch(error => {
                    console.log(error);
                    alert(JSON.stringify(error));
                });
            }
        }
    }
</script>

<style scoped>
    .create-memory {
        background: url('../../assets/Images/index.jpg');
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        position: fixed;
        background-size: 100% 100%;
        overflow: auto;
    }

    .circle {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }

    .form {
        width: 650px;
        height: 650px;
        border-radius: 50%;
    }

    .close {
        position: absolute;
        top: 120px;
        right: 150px;
    }

    .memory-title {
        width: 400px;
        position: absolute;
        top: 250px;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .memory-content {
        width: 400px;
        position: absolute;
        top: 340px;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .public {
        position: absolute;
        bottom: 160px;
        left: 150px;
    }

    .create {
        position: absolute;
        bottom: 140px;
        right: 120px;
        color: rgb(234, 182, 15);
    }

    .add {
        position: fixed;
        right: 250px;
        bottom: 50px;
        color: rgb(234, 182, 15);
    }

    .el-checkbox >>> .el-checkbox__inner {
        display: inline-block;
        position: relative;
        border: 1px solid #DCDFE6;
        border-radius: 2px;
        box-sizing: border-box;
        width: 20px;
        height: 20px;
        background-color: #FFF;
        z-index: 1;
        transition: border-color .25s cubic-bezier(.71,-.46,.29,1.46),background-color .25s cubic-bezier(.71,-.46,.29,1.46);
    }

    .el-checkbox >>> .el-checkbox__label {
        font-size: 24px;
        color: #00aaff;
    }
</style>