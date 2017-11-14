<template>
  <div class="col-md-5">
    <app-graph-holder
      name='mz'
      :experiments_data="experiments_data_rt"
      :selection_values="rt_selection_values"
      @selection_changed="rt_selection_change($event)">
    </app-graph-holder>
    <app-graph-holder
      name='rt'
      :experiments_data="experiments_data_mz"
      :selection_values="mz_selection_values"
      @selection_changed="mz_selection_change($event)">
    </app-graph-holder>
  </div>
</template>

<script>
import appGraphHolder from './AppGraphHolder.vue'
import axios from "axios"

export default {
  props: [
    'selectedBaseExperiment',
    'selectedCompareExperiment',
    'selectedRtMz',
    'resetTrigger'
  ],
  data () {
    return {
      experiments_data_rt: [],
      experiments_data_mz: [],
      rt_selection_values: {min:0, max:0},
      mz_selection_values: {min:0, max:0}
    }
  },
  methods: {
      pointSelected(e) {
          // sets lower and upper bounds variables, based on selection in the
          // 3D surface plot
          var rt_min = this.selectedRtMz.rt_lower,
              rt_max = this.selectedRtMz.rt_upper

          var mz_min = this.selectedRtMz.mz_lower,
              mz_max = this.selectedRtMz.mz_upper

          this.mz_selection_change({min: mz_min, max: mz_max})
          this.rt_selection_change({min: rt_min, max: rt_max})
      },
      rt_selection_change: function (e) {
        /* received a change in rt selection
        ensure API call and min max value communication
        expects e => { min: _, max: _ }
        */
        this.rt_selection_values = e
        // make an array of urls to call. Asume first selection is always filled
        let urlArray = [
                process.env.NODE_API + `experiments/` + this.selectedBaseExperiment + '/rt?low=' + e.min + '&high='+ e.max
              ]
        // add second url
        if (this.selectedCompareExperiment > 0) {
            urlArray.push(process.env.NODE_API + `experiments/` + this.selectedCompareExperiment + '/rt?low=' + e.min + '&high='+ e.max)
        }
        // create an array of promisses
        let promiseArray = urlArray.map(url => axios.get(url));
        let that = this;
        // call all promisses
        axios.all(promiseArray)
          .then(function(results) {
            that.experiments_data_rt = results.map(r => r.data.data);
          })
          .catch(error => {
            console.log(error)
          });
      },
      mz_selection_change: function (e) {
        /* received a change in mz selection
        ensure API call and min max value communication
        expects e => { min: _, max: _ }
        */
        // trigger the change of the sliders
        this.mz_selection_values = e
        // make an array of urls to call. Asume first selection is always filled
        let urlArray2 = [
                process.env.NODE_API + `experiments/` + this.selectedBaseExperiment + '/mz?low=' + e.min + '&high='+ e.max
              ]
        // add second url
        if (this.selectedCompareExperiment > 0) {
            urlArray2.push(process.env.NODE_API + `experiments/` + this.selectedCompareExperiment + '/mz?low=' + e.min + '&high='+ e.max)
        }
        // create an array of promisses
        let promiseArray = urlArray2.map(url => axios.get(url));
        let that = this;
        // call all promisses
        axios.all(promiseArray)
          .then(function(results) {
            that.experiments_data_mz = results.map(r => r.data.data);
          })
          .catch(error => {
            console.log(error)
          });
      }
  },
  watch: {
    selectedRtMz: function (e) {this.pointSelected(e)},
    resetTrigger: function () {
      this.experiments_data_rt = []
      this.experiments_data_mz =  []
      this.rt_selection_values = {min:0, max:0},
      this.mz_selection_values = {min:0, max:0}
    }
  },
  components: {
    'app-graph-holder': appGraphHolder
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
