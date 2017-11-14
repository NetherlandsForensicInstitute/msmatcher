<template>
  <div class="row">
    <app-menu
      :experiments="experiments"
      @base_selected='base_selected($event)'
      @compare_selected='compare_selected($event)'>
    </app-menu>
    <app-box-visuals
      :data="surfacetest"
      @rt_mz_selection_change="rt_mz_selection_change">
    </app-box-visuals>
    <app-graphs
      :selectedBaseExperiment="selectedBaseExperiment"
      :selectedCompareExperiment="selectedCompareExperiment"
      :selectedRtMz="selectedRtMz"
      :resetTrigger="resetTrigger">
    </app-graphs>
  </div>
</template>

<script>
import axios from "axios"
import appMenu from "./AppMenu.vue"
import appBoxVisual from "./BoxVisual.vue"
import appGraphs from "./AppGraphs.vue"

export default {
  data () {
    return {
      "experiments": [],
      "selectedBaseExperiment": -1,
      "selectedCompareExperiment": -1,
      "surfacetest": [],
      "selectedRtMz": [],
      "resetTrigger": 0
    }
  },
  methods: {
    get_experiments () {
      const path = process.env.NODE_API + `experiments`
      axios.get(path)
      .then(response => {
        this.experiments = response.data.experiments
      })
      .catch(error => {
        console.log(error)
      })
    },
    get_experiment_data (id) {
        const path = process.env.NODE_API + `experiments/` + id
        axios.get(path)
        .then(response => {
          this.surfacetest =
            {meta_data: response.data.meta,
                                graph_data: {
                z: response.data.intensities,
                              type: 'surface',
                              colorscale: [
                                ['0.0', 'rgb(220,220,220)'],
                                ['0.00001', 'rgb(220,220,220)'],
                                ['0.01', 'rgb(49,54,149)'],
                                ['1.0', 'rgb(49,54,149)']
                              ] }}
        })
        .catch(error => {
          console.log(error)
        })
    },
    base_selected (e) {
      // set the base id
      this.selectedBaseExperiment = e
      // empty the 3D plot and 2 D plots
      if ( e < 0 ) {
          this.surfacetest = {graph_data: {z: [[0,0]], type: "surface"}}
      } else {
        this.get_experiment_data(e)
      }
      (this.resetTrigger == 0 ) ? this.resetTrigger = 1 : this.resetTrigger = 0;
    },
    compare_selected (e) {
      this.selectedCompareExperiment = e;

      (this.resetTrigger == 0 ) ? this.resetTrigger = 1 : this.resetTrigger = 0;
    },
    rt_mz_selection_change (e) {
      // selection change received, signaling coordinate change
      this.selectedRtMz = e
    }
  },
  created () {
    this.get_experiments()
  },
  components: {
    "app-menu": appMenu,
    "app-box-visuals": appBoxVisual ,
    "app-graphs": appGraphs
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
