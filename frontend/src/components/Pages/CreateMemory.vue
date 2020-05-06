<template>
    <div class="create-memory">
        <el-button @click="back" class="button-back" style="width: 100px; top: 5px; left: 0; position: absolute;">
            BACK
        </el-button>
        <div class="form">
            <el-form :hide-required-asterisk="true"
                     :model="createMemoryForm"
                     :rules="createMemoryRules"
                     ref="createMemoryForm">
                <label style="font-size: 24px; color: rgb(234,213,15);">主题：{{ subjectName }}</label><br/>
                <el-form-item class="memory-title" prop="title">
                    <el-input style="height: 150px;" v-model="createMemoryForm.title"></el-input>
                </el-form-item>
                <el-form-item class="memory-title" prop="content">
                    <el-input class="memory-content"
                              rows="10"
                              type="textarea"
                              v-model="createMemoryForm.content"></el-input>
                </el-form-item>
                <div class="private">
                    <font-awesome-icon :icon="createMemoryForm.privacy ? ['far', 'eye-slash'] : ['far', 'eye']"
                                       :style="{color : createMemoryForm.privacy ? 'rgb(210,210,210)' : '#ffff00'}"
                                       @click="setPrivate"
                                       style="font-size: 22px;"></font-awesome-icon>
                    <label :style="{color : createMemoryForm.privacy ? 'rgb(210,210,210)' : '#ffff00'}"
                           @click="setPrivate"
                           class="text-button"
                           style="line-height: 30px; font-size: 22px;">
                        {{ createMemoryForm.privacy ? ' set private' : ' set public' }}</label>
                </div>
                <el-button @click="submit"
                           class="button-common create"
                           style="font-size: 24px;"
                           type="primary">
                    <font-awesome-icon icon="paper-plane"/>
                    CREATE
                </el-button>
            </el-form>
        </div>
        <div class="add">
            <el-popover
                    placement="top"
                    trigger="click"
                    width="150">
                <el-upload :before-upload="beforeUploadPicture"
                           :http-request="addPicture"
                           :limit="1"
                           :on-exceed="handlePictureExceed"
                           action="null">
                    <el-button>Add a picture</el-button>
                </el-upload>
                <br/>
                <el-upload :before-upload="beforeUploadAudio"
                           :http-request="addAudio"
                           :limit="1"
                           :on-exceed="handleAudioExceed"
                           action="null">
                    <el-button>Add an audio</el-button>
                </el-upload>
                <font-awesome-icon icon="plus-circle" slot="reference"/>
            </el-popover>
        </div>
    </div>
</template>

<script>
    import {library} from '@fortawesome/fontawesome-svg-core';
    import {faChevronLeft, faPaperPlane, faPlusCircle, faTimes} from '@fortawesome/free-solid-svg-icons';
    import CreateMemory from '../../graphql/CreateMemory/CreateMemory.graphql';
    import RefershToken from '../../graphql/RefreshToken.graphql';
    import error from '../../utils/error';

    library.add(faPlusCircle, faChevronLeft, faTimes, faPaperPlane);

    export default {
        name: 'CreateMemory',
        data() {
            return {
                subjectId: this.$route.params.subjectId,
                subjectName: this.$route.params.subjectName,
                createMemoryForm: {
                    title: '',
                    content: '',
                    privacy: true,
                    picture: null,
                    audio: null
                },
                createMemoryRules: {
                    title: [
                        {
                            required: true,
                            message: error.emptyTitle,
                            trigger: 'blur'
                        }
                    ],
                    content: [
                        {
                            required: true,
                            message: error.emptyContent,
                            trigger: 'blur'
                        }
                    ]
                }
            }
        },
        methods: {
            back() {
                this.$router.go(-1);
            },
            setPrivate() {
                this.createMemoryForm.privacy = !this.createMemoryForm.privacy;
            },
            beforeUploadPicture(file) {
                const fileType = file.name.split('.').pop();
                if (['jpg', 'png', 'gif'].indexOf(fileType) !== -1) {
                    return true;
                } else {
                    alert(error.wrongPicture);
                    return false;
                }
            },
            beforeUploadAudio(file) {
                const fileType = file.name.split('.').pop();
                if (['mp3', 'wav'].indexOf(fileType) !== -1) {
                    return true;
                } else {
                    alert(error.wrongAudio);
                    return false;
                }
            },
            handlePictureExceed() {
                alert(error.tooManyPictures);
            },
            handleAudioExceed() {
                alert(error.tooManyAudios);
            },
            addPicture(param) {
                this.createMemoryForm.picture = param.file;
            },
            addAudio(param) {
                this.createMemoryForm.audio = param.file;
            },
            submit() {
                this.$refs.createMemoryForm.validate((valid) => {
                    if (!valid) {
                        return;
                    }
                    this.refreshToken();
                })
            },
            refreshToken() {
                this.$apollo.mutate({
                    mutation: RefershToken,
                    variables: {
                        rtoken: localStorage.getItem('refreshToken')
                    }
                }).then(data => {
                    console.log(data.data);
                    if (data.data.refreshToken.success) {
                        localStorage.setItem('token', data.data.refreshToken.token);
                        localStorage.setItem('refreshToken', data.data.refreshToken.refreshToken);
                    }
                    this.createMemory();
                }).catch(error => {
                    console.log(error);
                });
            },
            createMemory() {
                const that = this;
                this.$apollo.mutate({
                    mutation: CreateMemory,
                    variables: {
                        memoryData: {
                            creatorUsername: JSON.parse(localStorage.getItem('user')).name,
                            title: this.createMemoryForm.title,
                            content: this.createMemoryForm.content,
                            privacy: this.createMemoryForm.privacy ? 0 : 1,
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
                        const memoryId = result.pid;
                        that.uploadPicture(memoryId, that.createMemoryForm.picture);
                    }
                }).catch(error => {
                    console.log(error);
                    alert(JSON.stringify(error));
                });
            },
            uploadPicture(memoryId, file) {
                if (!file) {
                    this.uploadAudio(memoryId, this.createMemoryForm.audio);
                    return
                }
                const data = new FormData();
                data.append('memoryid', memoryId.toString());
                data.append('files', file);
                const config = {
                    headers: {'Content-Type': 'multipart/form-data'}
                };
                const that = this;
                this.$axios.post('http://106.13.41.151/img/save/', data, config)
                    .then(response => {
                        console.log(response.data);
                        that.uploadAudio(memoryId, that.createMemoryForm.audio);
                    });
            },
            uploadAudio(memoryId, file) {
                if (!file) {
                    this.$router.push('mymemories');
                    return
                }
                const data = new FormData();
                data.append('memoryid', memoryId.toString());
                data.append('files', file);
                const config = {
                    headers: {'Content-Type': 'multipart/form-data'}
                };
                this.$axios.post('http://106.13.41.151/img/save/', data, config)
                    .then(response => {
                        console.log(response.data);
                        this.$router.push('mymemories');
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

    .form {
        width: 650px;
        height: 650px;
        border-radius: 50%;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
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
        top: 100px;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .private {
        position: absolute;
        bottom: 100px;
        left: 100px;
    }

    .create {
        position: absolute;
        bottom: 100px;
        right: 100px;
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
        transition: border-color .25s cubic-bezier(.71, -.46, .29, 1.46), background-color .25s cubic-bezier(.71, -.46, .29, 1.46);
    }

    .el-checkbox >>> .el-checkbox__label {
        font-size: 24px;
        color: #00aaff;
    }
</style>