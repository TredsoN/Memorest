<template>
    <div id="app">
        <router-view class="view-main" v-if="isRouterAlive"></router-view>
    </div>
</template>

<script>
    export default {
        name: 'App',
        provide() {
            return {
                reload: this.reload
            }
        },
        data() {
            return {
                isRouterAlive: true
            }
        },
        methods: {
            reload() {
                this.isRouterAlive = false;
                this.$nextTick(function () {
                    this.isRouterAlive = true
                })
            }
        }
    }
</script>

<style>
    #app {
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
    }
    div.background1 {
        background:url("./assets/Images/Image1.jpg");
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        position:fixed;
        background-size:100% 100%;
        overflow: auto;
    }
    div.background2 {
        background:url("./assets/Images/Image2.jpg");
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        position:fixed;
        background-size:100% 100%;
        overflow: auto;
    }
    div.el-input {
        opacity: 0.6;
    }
    div.el-form-item__error {
        font-size: 16px;
    }
    button.button-inputside {
        outline: none;
        color: rgb(234,182,15);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-inputside:hover {
        color: rgb(234,182,15);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-inputside:focus {
        color: rgb(234,182,15);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-inputside:disabled {
        outline: none;
        color: gray;
        background-color: transparent;
        border-color: transparent;
    }
    button.button-inputside:disabled:hover {
        color: gray;
        background-color: transparent;
        border-color: transparent;
    }
    button.button-back {
        font-size: 18px;
        outline: none;
        color: rgb(155,133,21);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-back:hover {
        color: rgb(155,133,21);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-back:focus {
        color: rgb(155,133,21);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common {
        outline: none;
        color: rgb(234,213,15);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common:hover {
        color: rgb(234,182,15);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common:focus {
        color: rgb(234,213,15);
        background-color: transparent;
        border-color: transparent;
    }
    i.form-label {
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 24px;
        color: rgb(234,213,15);
    }
    label.title {
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 32px;
        color: rgb(234,213,15);
    }
    label.content-title {
        line-height: 50px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 24px;
        color: rgb(234,213,15);
    }
    label.content-info {
        line-height: 50px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 24px;
        color: rgb(234,182,15);
    }
    hr.title {
        top: 50px;
        width: 100%;
        border: 1px solid rgb(234,213,15);
    }
</style>
