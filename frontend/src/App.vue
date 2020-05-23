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
    .div{
        background: black;
    }
    div.index {
        background: url('./assets/Images/index.jpg');
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        position: fixed;
        background-size: 100% 100%;
    }
    div.background1 {
        background:url("./assets/Images/Image1.jpg");
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        position:fixed;
        background-size:100% 100%;
    }
    div.background2 {
        background:url("./assets/Images/Image2.jpg");
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        position:fixed;
        background-size:100% 100%;
    }
    div.background3 {
        background: url('./assets/Images/Image3.jpg');
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        position: fixed;
        background-size: 100% 100%;
    }
    div.background4 {
        background: url('./assets/Images/Image4.jpg');
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        position: fixed;
        background-size: 100% 100%;
    }
    div.background5 {
        background: url('./assets/Images/Image5.jpg');
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        position: fixed;
        background-size: 100% 100%;
    }
    div.el-input, div.el-textarea {
        opacity: 0.6;
    }
    div.el-form-item__error {
        font-size: 18px;
    }
    input.el-input__inner, textarea.el-textarea__inner {
        font-size: 18px;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
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
        color: rgb(234,213,15);
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
        color: rgb(234,182,15);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common:hover {
        color: rgb(234,213,15);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common:focus {
        color: rgb(234,182,15);
        background-color: transparent;
        border-color: transparent;
    }
    i.form-label {
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 24px;
        color: rgb(234,182,15);
    }
    label.title {
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 32px;
        color: rgb(234,182,15);
    }
    label.content-title {
        line-height: 50px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 24px;
        color: rgb(234,182,15);
    }
    label.content-info {
        line-height: 50px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 24px;
        color: rgb(234,213,15);
    }
    label.text-button {
        line-height: 50px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 24px;
        color: rgb(234,213,15);
    }
    label.text-button:hover {
        cursor: pointer;
    }
    hr.title {
        top: 50px;
        width: 100%;
        border: 1px solid rgb(234,182,15);
    }
    hr.titledead {
        top: 50px;
        width: 100%;
        border: 1px solid rgb(190,190,190);
    }
    div.page-panel {
        position: absolute;
        top: 50px;
        width: 700px;
        text-align:left;
        z-index: 10;
    }
    div.memorytile {
        text-align: center;
        margin-left: 25px;
        width: 650px;
        height: 100px;
        border-bottom: 1px solid rgb(156, 128, 35);
    }
    div.memorytile:hover {
        height: 100px;
        border-bottom: 1px solid rgb(234,213,15);
        cursor: pointer;
    }
    div.deadmemorytile {
        text-align: center;
        margin-left: 25px;
        width: 650px;
        height: 100px;
        border-bottom: 1px solid rgb(110, 110, 110);
    }
    div.deadmemorytile:hover {
        height: 100px;
        border-bottom: 1px solid rgb(190,190,190);
        cursor: pointer;
    }
    div.label-div {
        float:left;
        width:325px;
        height:50px;
        margin-top:25px
    }
    div.label-div:hover {
        cursor: pointer;
    }
    label.label-with-pointer {
        line-height: 50px;
        font-size: 24px;
        font-style: normal;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }
    label.label-with-pointer:hover {
        cursor: pointer;
    }
    .fade-enter-active, .fade-leave-active {
        transition: opacity 2s
    }
    .fade-enter, .fade-leave-to {
        opacity: 0
    }
</style>
