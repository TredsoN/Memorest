<template>
    <div class="index">
        <svg :width="screenHeight*0.9" :height="screenHeight*0.9" style="position:absolute" :style="{left:(screenWidth-screenHeight*0.9)/2,top:screenHeight*0.05}">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" stop-color="#000000"/>
                        <stop offset="90%" stop-color="#000000"/>
                        <stop offset="91%" stop-color="#ffff00"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle :cx="screenHeight*0.45" :cy="screenHeight*0.45" :r="screenHeight*0.45" :fill="radialGradient" />
                </mask>
            </defs>
            <rect width="100%" height="100%" fill="#ffff00" :mask="mask" />
        </svg>

        <el-form :hide-required-asterisk="true"
            :model="createMemoryForm"
            :rules="createMemoryRules"
            ref="createMemoryForm">
            <el-form-item prop="title" style="position:absolute;text-align:center;height:50px" :style="{width:screenHeight*0.6+'px', left:(screenWidth-screenHeight*0.6)/2+'px',top:screenHeight*0.25+'px'}">
                <el-input style="width:height:150px;" v-model="createMemoryForm.title" maxlength="12"></el-input>
            </el-form-item>
            <el-form-item prop="content" style="position:absolute;text-align:center" :style="{width:screenHeight*0.6+'px', left:(screenWidth-screenHeight*0.6)/2+'px',top:screenHeight*0.35+'px'}">
                <el-input
                    rows="8"
                    type="textarea"
                    v-model="createMemoryForm.content"></el-input>
            </el-form-item>
        </el-form>

        <div style="position:absolute" :style="{width:screenHeight*0.4+'px',height:screenHeight*0.1+'px',left:(screenWidth-screenHeight*0.4)/2+'px',top:screenHeight*0.15+'px'}">
            <label class="content-title">{{ subjectName!=''?'Topic: '+subjectName:'No Topic' }}</label>
        </div>
        <div style="position:absolute;text-align:right;line-height:30px;font-size:22px" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.4)/2+'px',top:screenHeight*0.71+'px'}">
            <label class="text-button" @click="submit" style="color:#ffff00">publish </label>
            <font-awesome-icon icon="paper-plane" @click="submit" style="color:#ffff00"/>
        </div>
        <div style="position:absolute;text-align:left;line-height:30px;font-size:22px" :style="{width:screenHeight*0.5+'px',height:screenHeight*0.05+'px',left:(screenWidth-screenHeight*0.6)/2+'px',top:screenHeight*0.71+'px'}">
            <font-awesome-icon :icon="createMemoryForm.privacy ? ['far', 'eye-slash'] : ['far', 'eye']"
                :style="{color : createMemoryForm.privacy ? 'rgb(210,210,210)' : '#ffff00'}"
                @click="setPrivate"></font-awesome-icon>
            <label :style="{color : createMemoryForm.privacy ? 'rgb(210,210,210)' : '#ffff00'}"
                @click="setPrivate"
                class="text-button">
                {{ createMemoryForm.privacy ? ' set private' : ' set public' }}</label>
        </div>
        <div @click="back" class="goto-grave-box" style="line-height:30px;font-size:24px;position:absolute;text-align:center;width:100px;height:50px" :style="{left:(screenWidth-100)/2+'px',top:screenHeight*0.8+'px'}">
            <font-awesome-icon icon="chevron-left"/>
            <label class="goto-grave-label"> BACK</label> 
        </div>

        <div class="add" :style="{top:screenHeight*0.95-80+'px',left:(screenWidth*0.5+screenHeight*0.45-80)+'px'}">
            <el-popover
                placement="top"
                trigger="click">
                <el-upload :before-upload="beforeUploadPicture"
                    :http-request="addPicture"
                    :limit="1"
                    :on-exceed="handlePictureExceed"
                    action="null">
                    <el-button class="upload-button">
                        Add a photo
                    </el-button>
                </el-upload>
                <br/>
                <el-upload :before-upload="beforeUploadAudio"
                           :http-request="addAudio"
                           :limit="1"
                           :on-exceed="handleAudioExceed"
                           action="null">
                    <el-button class="upload-button">
                        Add an audio
                    </el-button>
                </el-upload>
                <font-awesome-icon icon="plus-circle" slot="reference"/>
            </el-popover>
        </div>
    </div>
</template>

<script>
    import {library} from '@fortawesome/fontawesome-svg-core';
    import {faChevronLeft, faPaperPlane, faPlusCircle, faTimes} from '@fortawesome/free-solid-svg-icons';
    import {faEye, faEyeSlash} from '@fortawesome/free-regular-svg-icons';
    import CreateMemory from '../../graphql/CreateMemory/CreateMemory.graphql';
    import RefershToken from '../../graphql/RefreshToken.graphql';
    import errorNote from '../../utils/error';

    library.add(faEye, faEyeSlash, faPlusCircle, faChevronLeft, faTimes, faPaperPlane);

    export default {
        name: 'CreateMemory',
        data() {
            return {
                subjectId: this.$route.params.subjectId,
                subjectName: this.$route.params.subjectName,
                screenHeight: document.documentElement.clientHeight,
                screenWidth: document.documentElement.clientWidth,
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
                            message: errorNote.emptyTitle,
                            trigger: 'blur'
                        }
                    ],
                    content: [
                        {
                            required: true,
                            message: errorNote.emptyContent,
                            trigger: 'blur'
                        }
                    ]
                }
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
        computed: {
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
                    alert(errorNote.wrongPicture);
                    return false;
                }
            },
            beforeUploadAudio(file) {
                const fileType = file.name.split('.').pop();
                if (['mp3', 'wav'].indexOf(fileType) === -1) {
                    alert(errorNote.wrongAudio);
                    return false;
                } else if (file.size / 1024 / 1024 > 10) {
                    alert(errorNote.tooLargeAudio);
                    return false;
                }
                return true;
            },
            handlePictureExceed() {
                alert(errorNote.tooManyPictures);
            },
            handleAudioExceed() {
                alert(errorNote.tooManyAudios);
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
                    if (data.data.refreshToken.success) {
                        localStorage.setItem('token', data.data.refreshToken.token);
                        localStorage.setItem('refreshToken', data.data.refreshToken.refreshToken);
                        this.createMemory();
                    }
                    else {
                        alert(errorNote.validateExpired);
                        localStorage.removeItem('user');
                        localStorage.removeItem('token');
                        localStorage.removeItem('refreshToken');
                        this.$router.push({name:'index'});
                    }
                }).catch(error => {
                    console.log(error);
                    alert(errorNote.netWorkError);
                });
            },
            createMemory() {
                const that = this;
                var memoryData = null;
                if(this.subjectId == '')
                    memoryData = {
                        creatorUsername: JSON.parse(localStorage.getItem('user')).name,
                        title: this.createMemoryForm.title,
                        content: this.createMemoryForm.content,
                        privacy: this.createMemoryForm.privacy ? 1 : 0,
                        picture: '',
                        audio: '',
                    }
                else
                    memoryData = {
                        creatorUsername: JSON.parse(localStorage.getItem('user')).name,
                        title: this.createMemoryForm.title,
                        content: this.createMemoryForm.content,
                        privacy: this.createMemoryForm.privacy ? 0 : 1,
                        picture: '',
                        audio: '',
                        subjectId: this.subjectId,
                        subjectName: this.subjectName
                    }
                this.$apollo.mutate({
                    mutation: CreateMemory,
                    variables: {
                        memoryData: memoryData
                    },
                    client: 'withtoken'
                }).then(data => {
                    let result = data.data.createMemory;
                    if (!result.success) {
                        alert(JSON.stringify(result.errors));
                    } else {
                        const memoryId = result.pid;
                        that.uploadPicture(memoryId, that.createMemoryForm.picture);
                    }
                }).catch(error => {
                    console.log(error);
                    alert(errorNote.netWorkError);
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
                this.$axios.post('/img/save/', data, config)
                    .then(response => {
                        console.log(response.data);
                        that.uploadAudio(memoryId, that.createMemoryForm.audio);
                    });
            },
            uploadAudio(memoryId, file) {
                if (!file) {
                    alert("Published successfully!")
                    window.close()
                    return
                }
                const data = new FormData();
                data.append('memoryid', memoryId.toString());
                data.append('files', file);
                const config = {
                    headers: {'Content-Type': 'multipart/form-data'}
                };
                this.$axios.post('/img/save/', data, config)
                    .then(response => {
                        console.log(response.data);
                        alert("Published successfully!")
                        window.close()
                    });
            }
        }
    }
</script>

<style scoped>
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
    .add {
        position: fixed;
        font-size: 60px;
        color: rgba(255,255,0,0.6);
    }
    .add:hover {
        color: rgb(255,255,0);
        cursor: pointer;
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
    button.upload-button {
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 18px;
        width: 150px;
        color: rgb(234,213,15);
    }
    button.upload-button:hover {
        border-color: rgb(255,255,0);
        background-color: rgba(255,255,0,0.1);
    }
</style>