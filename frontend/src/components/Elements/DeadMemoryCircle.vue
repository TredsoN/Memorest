<template>
    <div>
        <svg  :width="randbigsize" :height="randbigsize" style="position:absolute;left:0;top:0">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" stop-color="rgb(190,190,190)"/>
                        <stop offset="80%" stop-color="rgb(190,190,190)"/>
                        <stop offset="81%" stop-color="rgb(110,110,110)"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle :cx="randbigsize/2" :cy="randbigsize/2" :r="randbigsize/2" :fill="radialGradient" />
                </mask>
            </defs>
            <rect width="100%" height="100%" fill="rgb(110,110,110)" :mask="mask" />
            <text x="50%" y="50%" fill="rgb(225,225,225)" :style="{fontSize:contentFontSize+'px'}">{{ title }}</text>
        </svg>
    </div>
</template>

<script>
    export default {
        name: 'MemoryCircle',
        data() {
            return {
            }
        },
        props: {
            title: String,
            displayId: Number
        },
        computed: {
            randbigsize() {
                return 200+Math.random()*50;
            },
            contentFontSize() {
                if(this.title.length<=6)
                    return 24;
                else if(this.title.length<=10)
                    return 20;
                else
                    return 16;
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