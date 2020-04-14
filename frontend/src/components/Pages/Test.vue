<template>
    <div id="test">
        <input v-model="message"/>
        <p>{{message}}</p>
    </div>
</template>

<script>
export default {
    name:"Test",
    data(){
        return{
            message: ""
        }
    }
}
</script>