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
    div.el-input {
        opacity: 0.6;
    }
    button.button-inputside {
        font-size: 24px;
        outline: none;
        color: rgb(154,132,21);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-inputside:hover {
        color: rgb(154,132,21);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-inputside:focus {
        color: rgb(154,132,21);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common {
        font-size: 32px;
        outline: none;
        color: rgb(234,213,15);
        background-color: transparent;
        border-color: transparent;
    }
    button.button-common:hover {
        color: rgb(234,213,15);
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
        font-size: 32px;
        color: rgb(234,213,15);
    }
</style>
