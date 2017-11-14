<template>
  <div>
    <app-graph :name="name" :experiments_data="experiments_data"></app-graph>
    <app-slider
        :name="name"
        :min="0"
        :max="500"
        :selection_values="selection_values"
        @selection_changed="selection_changed($event)">
      </app-slider>
  </div>
</template>

<script>
import appGraph from './AppGraph.vue'
import appSlider from './AppSlider.vue'

export default {
  props: [
    'name',
    'experiments_data',
    'selection_values'
  ],
  data () {
    return {
    }
  },
  computed: {
    min_value: function() { return this.selection_values.min},
    max_value: function() { return this.selection_values.max}
  },
  components : {
    'app-graph': appGraph,
    'app-slider': appSlider
  },
  methods: {
    selection_changed: function(e) {
      // passing the selection change straight up..
      this.$emit("selection_changed", e)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
