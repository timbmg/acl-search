<template>
    <div>
        <div class="row">
            <div class="col-3">
                <a class="filter text-secondary" data-bs-toggle="collapse" href="#collapseYearFilter" aria-expanded="false" aria-controls="collapseYearFilter">
                   <i class="bi bi-filter"></i> Year {{minYear}} - {{maxYear}}
                </a>
                <div class="collapse" id="collapseYearFilter">
                    <div class="row gy-3">
                        <div class="col-6">
                            <input type="number" v-model="minYear" :min="minRange" :max="maxRange" class="form-control" @input="onUpdateMinMaxValue($event, 'min')">
                        </div>
                        <div class="col-6">
                            <input type="number" v-model="maxYear" :min="minRange" :max="maxRange" class="form-control" @input="onUpdateMinMaxValue($event, 'max')">
                        </div>
                        <div class="col-12">
                            <div id="slider" ref="slider" class="slider-styled noUi-sm noUi-value-sub"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import noUiSlider from 'nouislider';
import wNumb from 'wnumb';
export default {
    data() {
        return {
            minRange: 1958,
            maxRange: new Date().getFullYear(),
            minYear: new Date().getFullYear() - 5,
            maxYear: new Date().getFullYear()
        }
    },
    mounted() {
        var slider = document.getElementById('slider');
        noUiSlider.create(slider, {
            start: [this.minYear, this.maxYear],
            // tooltips: true,
            connect: true,
            step: 1,
            range: {
                'min': [this.minRange, 1],
                '30%': [this.maxRange-10, 1],
                'max': this.maxRange
            },
            pips: {
                mode: 'range',
                density: 5,
                format: wNumb({
                    decimals: 0
                })
            }
        });

        this.$refs.slider.noUiSlider.on('update',(values, handle) => {
            this[handle ? 'maxYear' : 'minYear'] = parseInt(values[handle]);
        });
    },
    methods: {
        onUpdateMinMaxValue(e, x) {
            if (x == 'min') {
                this.minYear = e.target.value;
            } else {
                this.maxYear = e.target.value;
            }
            // console.log(e.target.value);
            // console.log(x);
            // console.log(this.minValue);
            // console.log(this.maxValue);
            this.$refs.slider.noUiSlider.set([this.minYear, this.maxYear]);
        }
    },
    watch: {
        minYear: {
            immediate: true,
            handler() {
                this.$emit('yearUpdate', [this.minYear, this.maxYear]);
                // if (this.minYear >= this.minRange && this.minYear <= this.maxYear) {
                // }
            },
        },
        maxYear: {
            immediate: false,
            handler() {
                this.$emit('yearUpdate', [this.minYear, this.maxYear]);
            }
        }
    }
}
</script>

<style>
.filter {
    color: var(--bs-primary);

}
#slider {
    height: 10px;
    
}
.noUi-connect {
    background: var(--bs-primary);
    
}
.noUi-value-sub {
    color: var(--bs-primary);
    font: var(--font-family-sans-serif);
    /* font-size: 14px; */
}
.slider-styled,
.slider-styled .noUi-handle {
    box-shadow: none;
    
}

#slider .noUi-handle {
    height: 18px;
    width: 18px;
    top: -5px;
    right: -9px; /* half the width */
    border-radius: 9px;
}

/* Hide markers on slider handles */
.slider-styled .noUi-handle::before,
.slider-styled .noUi-handle::after {
    display: none;
}

</style>
