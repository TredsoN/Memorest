<template>
    <div @mouseenter="ishover = true" @mouseleave="ishover = false">
        <svg v-if="!ishover" :width="randsize" :height="randsize" style="position:absolute" :style="{top:(randbigsize-randsize)/2+'px',left:(randbigsize-randsize)/2+'px'}">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" stop-color="rgb(110,110,110)"/>
                        <stop offset="40%" stop-color="rgb(110,110,110)"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle :cx="randsize/2" :cy="randsize/2" :r="randsize/2" :fill="radialGradient" />
                </mask>
            </defs>
            <rect width="100%" height="100%" fill="rgb(110,110,110)" :mask="mask" />
        </svg>
        <svg v-if="ishover" :width="randbigsize" :height="randbigsize" style="position:absolute;left:0;top:0">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" stop-color="rgb(190,190,190)"/>
                        <stop offset="90%" stop-color="rgb(190,190,190)"/>
                        <stop offset="91%" stop-color="rgb(110,110,110)"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle :cx="randbigsize/2" :cy="randbigsize/2" :r="randbigsize/2" :fill="radialGradient" />
                </mask>
            </defs>
            <rect width="100%" height="100%" fill="rgb(110,110,110)" :mask="mask" />
            <text x="50%" y="50%" fill="rgb(225,225,225)" style="fontSize: xx-large">{{ title }}</text>
        </svg>
    </div>
</template>

<script>
    export default {
        name: 'MemoryCircle',
        data() {
            return {
                ishover: false
            }
        },
        props: {
            title: String,
            displayId: Number
        },
        computed: {
            randsize() {
                return 20+Math.random()*10;
            },
            randbigsize() {
                return 150+Math.random()*100;
            },
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
        }
    }
</script>

<style scoped>
    text {
        text-anchor: middle;
    }
</style>