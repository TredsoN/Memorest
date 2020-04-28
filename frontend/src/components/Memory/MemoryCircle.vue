<template>
    <div>
        <svg :width="exactSize" :height="exactSize">
            <defs>
                <defs>
                    <radialGradient :id="radialGradientId">
                        <stop offset="0%" :stop-color="exactColor"/>
                        <stop offset="80%" :stop-color="exactColor"/>
                        <stop offset="100%" stop-color="#000000"/>
                    </radialGradient>
                </defs>
                <mask :id="maskId">
                    <circle :cx="exactSize / 2" :cy="exactSize / 2" :r="exactSize / 2" :fill="radialGradient" />
                    <circle :cx="exactSize / 2" :cy="exactSize / 2" :r="radius" :fill="innerColor" />
                </mask>
            </defs>
            <rect width="100%" height="100%" :fill="fillColor" :mask="mask" />
            <text x="50%" y="50%" :fill="exactColor" :style="{ fontSize: fontSize }">{{ title }}</text>
        </svg>
    </div>
</template>

<script>
    export default {
        name: 'MemoryCircle',
        props: {
            title: {
                type: String,
                default: ''
            },
            size: {
                type: String,
                validator: function (value) {
                    return ['small', 'medium', 'large', 'x-large'].indexOf(value) !== -1
                }
            },
            color: {
                type: String,
                validator: function (value) {
                    return ['light-yellow', 'dark-yellow', 'light-blue', 'dark-blue'].indexOf(value) !== -1
                }
            },
            displayId: {
                type: Number,
                default: 0
            }
        },
        computed: {
            exactSize() {
                switch (this.size) {
                    case 'x-large':
                        return 650;
                    case 'large':
                        return 220;
                    case 'medium':
                        return 180;
                    case 'small':
                        return 150;
                }
                return 180;
            },
            radius() {
                switch (this.size) {
                    case 'x-large':
                        return this.exactSize / 2 - 50;
                    case 'large':
                        return this.exactSize / 2 - 25;
                    case 'medium':
                        return this.exactSize / 2 - 22;
                    case 'small':
                        return this.exactSize / 2 - 18;
                }
                return 150;
            },
            exactColor() {
                switch (this.color) {
                    case 'light-yellow':
                    case 'dark-yellow':
                        return '#ffff00';
                    case 'light-blue':
                    case 'dark-blue':
                        return '#00aaff';
                }
                return '#ffff00';
            },
            innerColor() {
                switch (this.color) {
                    case 'light-yellow':
                    case 'dark-yellow':
                        return '#666600';
                    case 'light-blue':
                    case 'dark-blue':
                        return '#004466';
                }
                return '#666600';
            },
            fillColor() {
                switch (this.color) {
                    case 'light-yellow':
                        return 'rgba(255, 255, 0, 0.6)';
                    case 'dark-yellow':
                        return 'rgba(255, 255, 0, 0.3)';
                    case 'light-blue':
                        return 'rgba(0, 170, 255, 0.6)';
                    case 'dark-blue':
                        return 'rgba(0, 170, 255, 0.3)';
                }
                return 'rgba(255, 255, 0, 0.6)';
            },
            fontSize() {
                switch (this.size) {
                    case 'small':
                        return 'large';
                    case 'medium':
                        return 'x-large';
                    case 'large':
                        return 'xx-large';
                }
                return 'x-large';
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
        dominant-baseline: middle;
        text-anchor: middle;
    }
</style>