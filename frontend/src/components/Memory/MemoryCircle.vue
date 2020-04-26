<template>
    <div @mouseenter="ishover = true" @mouseleave="ishover = false">
        <svg v-if="!ishover" :width="randsize" :height="randsize" style="position:absolute" :style="{top:(200-randsize)/2+'px',left:(200-randsize)/2+'px'}">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" :stop-color="exactColor"/>
                        <stop offset="40%" :stop-color="exactColor"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle :cx="randsize/2" :cy="randsize/2" :r="randsize/2" :fill="radialGradient" />
                </mask>
            </defs>
            <rect width="100%" height="100%" :fill="fillColor" :mask="mask" />
        </svg>
        <svg v-if="ishover" width="200" height="200" style="position:absolute;left:0;top:0">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" :stop-color="innerColor"/>
                        <stop offset="90%" :stop-color="innerColor"/>
                        <stop offset="91%" :stop-color="exactColor"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle cx="100" cy="100" r="100" :fill="radialGradient" />
                </mask>
            </defs>
            <rect width="100%" height="100%" :fill="fillColor" :mask="mask" />
            <text x="50%" y="50%" :fill="exactColor" style="fontSize: xx-large">{{ title }}</text>
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
            subject: String,
            opacity: Number,
            displayId: Number
        },
        computed: {
            randsize() {
                return 20+Math.random()*10;
            },
            exactColor() {
                if (this.subject == "null")
                    return '#ffff00';   
                return '#00aaff';
            },
            innerColor() {
                if (this.subject == "null") 
                    return 'rgba(255, 255, 0, 0.2)';
                return 'rgba(0, 170, 255, 0.2)';
            },
            fillColor() {
                if (this.subject == "null")
                    return 'rgba(255, 255, 0, '+this.opacity+')';   
                return 'rgba(0, 170, 255, '+this.opacity+')';
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