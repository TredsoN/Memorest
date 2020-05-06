<template>
    <div class="select-subject">
        <el-button @click="back" class="button-back" style="width: 100px; top: 5px; left: 0; position: absolute;">
            BACK
        </el-button>
        <div v-if="!isLogined">
            <label style="font-size: 36px; color: rgb(234,213,15);">{{ loginBeforeCreateMemory }}</label><br/>
            <router-link :to="{ name: 'login' }">
                <el-button class="button-common" style="font-size: 24px;">LOGIN</el-button>
            </router-link>
        </div>
        <div v-else>
            <el-select filterable placeholder="PLEASE SELECT A TOPIC" v-model="subject">
                <el-option
                        :key="subject.id"
                        :label="subject.name"
                        :value="subject.id"
                        v-for="subject in subjects">
                </el-option>
            </el-select>
            <br/><br/>
            <el-button @click="selectSubject">OK</el-button>
        </div>
    </div>
</template>

<script>
    import SearchSubject from '../../graphql/SelectSubject/SearchSubject.graphql';
    import error from '../../utils/error';

    export default {
        name: 'SelectSubject',
        data() {
            return {
                isLogined: localStorage.getItem('token'),
                loginBeforeCreateMemory: error.loginBeforeCreateMemory,
                subject: '',
                subjects: []
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
                console.log(result);
                if (!result.success) {
                    alert(JSON.stringify(result.errors));
                } else {
                    that.subjects = result.subjects;
                }
            }).catch(error => {
                console.log(error);
                alert(JSON.stringify(error));
            });
        },
        methods: {
            back() {
                this.$router.go(-1);
            },
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
            }
        }
    }
</script>

<style scoped>
    .select-subject {
        background: url('../../assets/Images/index.jpg');
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        position: fixed;
        background-size: 100% 100%;
        overflow: auto;
    }
</style>