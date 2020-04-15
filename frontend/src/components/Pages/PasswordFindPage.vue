<template>
    <div>
        <button @click="goBack">返回</button>
        <input v-model="email" placeholder="输入邮箱"/>
        <label>{{warning1}}</label>
        <button @click="getcode">获取验证码</button>
        <input v-model="newpassword1" placeholder="输入新密码"/>
        <label>{{warning2}}</label>
        <input v-model="newpassword2" placeholder="再次输入新密码"/>
        <label>{{warning2}}</label>
        <button @click="submit">确定</button>
    </div>
</template>

<script>
export default {
    data() {
        return{
            email: '',
            newpassword1: '',
            newpassword2: '',
            warning1: '',
            warning2: '',
            warning3: ''
        }
    },
    methods: {
        getcode() {
            var myReg=/^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/;
            if(!myReg.test(this.email)){
                this.warning1 = '邮箱格式不正确';
                return;
            }
        },
        submit() {
            
        },
        goBack() {
            this.$router.go(-1);
        }
    }
}
</script>