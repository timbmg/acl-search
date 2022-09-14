<template>
    <div>
        <div class="row">
            <div class="col-auto dropdown">
                <!-- <button type="button" class="btn btn-link btn-outline-dark  dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false"><i class="bi bi-filter"></i> Year {{minYear}} - {{maxYear}}</button> -->
                <div class="dropdown-toggle" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
                    <!-- <i class="bi bi-filter"></i>  -->
                    Year: {{minYear}} - {{maxYear}}
                </div>
                <div class="dropdown-menu p-4 text-muted" style="width: 240px; min-height: 150px">
                    <div class="row gy-3">
                        <div class="col-6">
                            <input type="number" v-model="minYear" :min="minRange" :max="maxRange" class="form-control year-input" @input="onUpdateMinMaxValue($event, 'min')">
                        </div>
                        <div class="col-6">
                            <input type="number" v-model="maxYear" :min="minRange" :max="maxRange" class="form-control year-input" @input="onUpdateMinMaxValue($event, 'max')">
                        </div>
                        <div class="col-12">
                            <div id="slider" ref="slider" class="slider-styled noUi-sm noUi-value-sub"></div>
                        </div>
                    </div>
                </div>

            </div>
            
            <div class="col-auto dropdown">
                <div class="dropdown-toggle" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false">
                    <!-- <i class="bi bi-filter"></i>  -->
                    Venues
                </div>
                <div class="dropdown-menu p-2 text-muted">
                    <div class="row gx-0">
                        <div class="form-check form-check-inline venue-checkbox">
                            <input class="form-check-input" type="checkbox" name="group-topLevel"  value="group-topLevel" id="group-topLevel" v-model="topLevelCheckboxes" @change="onVenueCheckboxChange($event)">
                            <label class="form-check-label" for="group-topLevel">
                                <h6>Top-Level</h6>
                            </label>
                        </div>
                        <div v-for="(venue, venueIndex) in topLevelVenues" :key="venueIndex" class="col-4 form-check form-check-inline venue-checkbox">
                            <input class="form-check-input" type="checkbox" :value="venue.acronym" :id="venue.acronym" v-model="selectedVenues" @change="onVenueCheckboxChange($event)">
                            <label class="form-check-label" :for="venue.acronym">
                                <span class="tooltip-test" :title="venue.name">{{venue.acronym}}</span>
                            </label>
                        </div>
                        <li><hr class="dropdown-divider"></li>
                        <div class="form-check form-check-inline venue-checkbox">
                            <input class="form-check-input" type="checkbox" name="group-acl"  value="group-acl" id="group-acl" v-model="topLevelCheckboxes" @change="onVenueCheckboxChange($event)">
                            <label class="form-check-label" for="group-acl" >
                                <h6>ACL</h6>
                            </label>
                        </div>
                        <div v-for="(venue, venueIndex) in aclNotTopLevelVenues" :key="venueIndex" class="col-4 form-check form-check-inline venue-checkbox">
                            <input class="form-check-input" type="checkbox" :value="venue.acronym" :id="venue.acronym" v-model="selectedVenues" @change="onVenueCheckboxChange($event)">
                            <label class="form-check-label" :for="venue.acronym">
                                <span class="tooltip-test" :title="venue.name">{{venue.acronym}}</span>
                            </label>
                        </div>
                        <li><hr class="dropdown-divider"></li>
                        <div class="form-check form-check-inline venue-checkbox">
                            <input class="form-check-input" type="checkbox" name="group-all"  value="group-all" id="group-all"  v-model="topLevelCheckboxes" @change="onVenueCheckboxChange($event)">
                            <label class="form-check-label" for="group-all" >
                                <h6>All</h6>
                            </label>
                        </div>
                        <div v-for="(venue, venueIndex) in remainingVenues" :key="venueIndex" class="col-4 form-check form-check-inline venue-checkbox">
                            <input class="form-check-input" type="checkbox" :value="venue.acronym"  :id="venue.acronym" v-model="selectedVenues" @change="onVenueCheckboxChange($event)">
                            <label class="form-check-label" :for="venue.acronym">
                                <span class="venue-checkbox tooltip-test" :title="venue.name">{{venue.acronym}}</span>
                            </label>
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
    props: {
        venues: {
            type: Array
        },
    },
    data() {
        return {
            minRange: 1958,
            maxRange: new Date().getFullYear(),
            minYear: new Date().getFullYear() - 5,
            maxYear: new Date().getFullYear(),
            selectedVenues: new Set(),
            topLevelCheckboxes: new Set(["group-topLevel"]),
            topLevelVenues: [],
            aclNotTopLevelVenues: [],
            remainingVenues: [],
            topLevelVenuesAcronyms: [],
            aclNotTopLevelVenuesAcronyms: [],
            remainingVenuesAcronyms: []
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
            this.$refs.slider.noUiSlider.set([this.minYear, this.maxYear]);
        },
        onVenueCheckboxChange(e) {
            // console.log(e.target.value);
            if (e.target.value.startsWith("group-")) {
                if (e.target.value == "group-topLevel") {
                    if (e.target.checked) {
                        this.topLevelVenuesAcronyms.forEach(venue => this.selectedVenues.add(venue));
                        this.topLevelCheckboxes.add("group-topLevel");
                    } else {
                        this.topLevelVenuesAcronyms.forEach(venue => this.selectedVenues.delete(venue));
                        this.topLevelCheckboxes.delete("group-topLevel");
                    }
                } else if (e.target.value == "group-acl") {
                    if (e.target.checked) {
                        this.aclNotTopLevelVenuesAcronyms.forEach(venue => this.selectedVenues.add(venue));
                        this.topLevelCheckboxes.add("group-acl");
                    } else {
                        this.aclNotTopLevelVenuesAcronyms.forEach(venue => this.selectedVenues.delete(venue));
                        this.topLevelCheckboxes.delete("group-acl");
                    }
                } else if (e.target.value == "group-all") {
                    if (e.target.checked) {
                        this.remainingVenuesAcronyms.forEach(venue => this.selectedVenues.add(venue));
                        this.topLevelCheckboxes.add("group-all");
                    } else {
                        this.remainingVenuesAcronyms.forEach(venue => this.selectedVenues.delete(venue));
                        this.topLevelCheckboxes.delete("group-all");
                    }
                } 
            }
            this.$emit('venuesUpdate', this.selectedVenues);
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
        },
        venues: {
            immediate: true,
            handler() {
                // this.aclVenues = this.venues.filter(venue => venue.is_acl).map(venue => venue.acronym);
                this.topLevelVenues = this.venues.filter(venue => venue.is_toplevel);
                this.aclNotTopLevelVenues = this.venues.filter(venue => !venue.is_toplevel && venue.is_acl);
                this.remainingVenues = this.venues.filter(venue => !(venue.is_toplevel || venue.is_acl));
                this.topLevelVenuesAcronyms = this.venues.filter(venue => venue.is_toplevel).map(venue => venue.acronym);
                this.aclNotTopLevelVenuesAcronyms = this.venues.filter(venue => !venue.is_toplevel && venue.is_acl).map(venue => venue.acronym);
                this.remainingVenuesAcronyms = this.venues.filter(venue => !(venue.is_toplevel || venue.is_acl)).map(venue => venue.acronym);
                
                // set default selected venues
                this.topLevelVenuesAcronyms.forEach(venue => this.selectedVenues.add(venue));
                this.$emit('venuesUpdate', this.selectedVenues);
            }
        }
    }
}
</script>

<style>
.filter {
    color: var(--bs-primary);

}
.year-input {
    max-width: 84px;
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
.dropdown-menu {
    width: 360px;
    max-height: 360px;
    overflow-y: auto;
}
.venue-checkbox {
    margin-right: 0;
    /* overflow:hidden; */
    white-space:nowrap;
    -ms-text-overflow: ellipsis;
    -o-text-overflow: ellipsis;
    text-overflow: ellipsis;
    display: inline-block;
    display:block;
}

</style>
