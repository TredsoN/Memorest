<template>
    <div class="index">
        <svg :width="screenHeight*0.9" :height="screenHeight*0.9" style="position:absolute" :style="{left:(screenWidth-screenHeight*0.9)/2,top:screenHeight*0.05}">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" stop-color="#000000"/>
                        <stop offset="90%" stop-color="#000000"/>
                        <stop offset="91%" stop-color="#00aaff"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle :cx="screenHeight*0.45" :cy="screenHeight*0.45" :r="screenHeight*0.45" :fill="radialGradient" />
                </mask>
            </defs>
            <rect width="100%" height="100%" fill="#00aaff" :mask="mask" />
        </svg>

        <div style="position:absolute" :style="{width:screenHeight*0.6+'px',height:screenHeight*0.4+'px',left:(screenWidth-screenHeight*0.6)/2+'px',top:screenHeight*0.35+'px'}">
            <el-button @click="selectSubjectTop(0)" class="button-common-blue" style="font-size:18px;position:absolute" :style="{top:screenHeight*0.01+'px',left:screenHeight*0.02+'px'}">
                {{subjects[0].name}}
            </el-button>
            <el-button @click="selectSubjectTop(1)" class="button-common-blue" style="font-size:20px;position:absolute" :style="{top:screenHeight*0.3+'px',left:screenHeight*0.06+'px'}">
                {{subjects[1].name}}
            </el-button>
            <el-button @click="selectSubjectTop(2)" class="button-common-blue" style="font-size:24px;position:absolute" :style="{top:screenHeight*0.15+'px',left:screenHeight*0.15+'px'}">
                {{subjects[2].name}}
            </el-button>
            <el-button @click="selectSubjectTop(3)" class="button-common-blue" style="font-size:16px;position:absolute" :style="{top:screenHeight*0.06+'px',left:screenHeight*0.4+'px'}">
                {{subjects[3].name}}
            </el-button>
            <el-button @click="selectSubjectTop(4)" class="button-common-blue" style="font-size:18px;position:absolute" :style="{top:screenHeight*0.2+'px',left:screenHeight*0.5+'px'}">
                {{subjects[4].name}}
            </el-button>
            <el-button @click="selectSubjectTop(5)" class="button-common-blue" style="font-size:22px;position:absolute" :style="{top:screenHeight*0.16+'px',left:-screenHeight*0.1+'px'}">
                {{subjects[5].name}}
            </el-button>
        </div>
        <div style="position:absolute" :style="{width:screenHeight*0.4+'px',height:screenHeight*0.1+'px',left:(screenWidth-screenHeight*0.4)/2+'px',top:screenHeight*0.15+'px'}">
            <label class="content-title-blue" style="word-break:break-all;font-size:36px;line-height:30px">
                Choose A Topic
            </label>
        </div>
        <div style="position:absolute;text-align:center;height:50px" :style="{width:screenHeight*0.5+'px', left:(screenWidth-screenHeight*0.5)/2+'px',top:screenHeight*0.25+'px'}">
            <el-select filterable :style="{width:screenHeight*0.5+'px'}" placeholder="Select a topic." v-model="subject">
                <el-option
                    :key="subject.id"
                    :label="subject.name"
                    :value="subject.id"
                    v-for="subject in subjects">
                </el-option>
            </el-select>
        </div>
        <div @click="selectSubject" class="goto-grave-box-blue" style="line-height:30px;font-size:24px;position:absolute;text-align:center;width:100px;height:50px" :style="{left:(screenWidth-100)/2+'px',top:screenHeight*0.8+'px'}">
            <label class="goto-grave-label">
                {{subject==''?'SKIP ':'NEXT '}}
            </label>
            <font-awesome-icon icon="chevron-right"/>
        </div>
    </div>
</template>

<script>
    import SearchSubject from '../../graphql/SelectSubject/SearchSubject.graphql';
    import { library } from '@fortawesome/fontawesome-svg-core';
    import { faChevronRight } from '@fortawesome/free-solid-svg-icons';

    library.add(faChevronRight);

    export default {
        name: 'SelectSubject',
        data() {
            return {
                subject: '',
                subjects: [],
                screenHeight: document.documentElement.clientHeight,
                screenWidth: document.documentElement.clientWidth
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
        mounted() {
            const that = this;
            this.$apollo.mutate({
                mutation: SearchSubject,
                variables: {
                    keyword: ''
                }
            }).then(data => {
                let result = data.data.searchSubject;
                if (!result.success) {
                    alert(JSON.stringify(result.errors));
                } else {
                    that.subjects = result.subjects;
                }
            }).catch(error => {
                console.log(error);
                alert('The network is not in good condition. Please try again later.');
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
            selectSubject() {
                let subjectName = '';
                for (let i = 0; i < this.subjects.length; i++) {
                    if (this.subject === this.subjects[i].id) {
                        subjectName = this.subjects[i].name;
                    }
                }
                this.$router.push({
                    name: 'createMemory',
                    params: {
                        subjectId: this.subject,
                        subjectName: subjectName
                    }
                })
            },
            selectSubjectTop(idx) {
                this.$router.push({
                    name: 'createMemory',
                    params: {
                        subjectId: this.subjects[idx].id,
                        subjectName: this.subjects[idx].name
                    }
                })
            }
        }
    }
</script>

<style>
    label.content-title-blue {
        line-height: 50px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 24px;
        color: rgb(0,170,255);
    }
    button.button-common-blue {
        outline: none;
        color: rgb(0,170,255);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common-blue:hover {
        color: rgb(0,110,233);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common-blue:focus {
        color: rgb(0,110,233);
        background-color: transparent;
        border-color: transparent;
    }
    .goto-grave-box-blue {
        position: fixed;
        color: rgb(0,170,255);
     }
    .goto-grave-box-blue:hover {
        cursor: pointer;
        color: rgb(0,110,233);
     }
</style>