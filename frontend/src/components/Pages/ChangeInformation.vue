<template>
    <div>
        <input v-model="newname" :placeholder="name"/>
        <p>{{newname}}</p>
        <button @click="submit"></button>
    </div>
</template>

<script>
import Vue from 'vue'
export default {
    inject: ['reload'],
    data() {
        return {
            name: Vue.prototype.$user.name,
            newname: ""
        }
    },
    methods:{
        submit() {
            Vue.prototype.$user.name = this.newname;
            alert(this.newname);
            this.reload();
        }
    }
}
</script>>