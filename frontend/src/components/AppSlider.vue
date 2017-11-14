<template>
  <div>
    <div :id='slider_name'></div>
    <p>{{mutable_min_value}} - {{mutable_max_value}}</p>
  </div>
</template>

<script>
export default {
  props: ["name", "min", "max", "selection_values"],
  data () {
    return {
      "slider_name": this.name + "-slider",
      "slider_amount": this.name + "-amount",
      "mutable_min_value": this.min_value,  // used to temporary store data for viz
      "mutable_max_value": this.max_value // used to temporary store data for viz
    }
  },
  computed: {

  },
  mounted () {
      $( "#" + this.slider_name ).slider({
        range: true,
        min: this.min,
        max: this.max,
        step: 0.01,
        values: [this.min, this.max],
        slide: function( event, ui ) {
          this.mutable_min_value = ui.values[0];
          this.mutable_max_value = ui.values[1];
        }.bind(this),
        stop: function(event, ui ) {
          this.selection_changed(ui.values[0], ui.values[1])
        }.bind(this)
      });
  },
  methods: {
    selection_changed: function (min_value, max_value) {
      // communicates changes in the data selection back up the line
      this.$emit("selection_changed", {min: min_value, max: max_value})
    }
  },
  watch: {
    selection_values: function(e) {
      // set the slider min en max values
      this.mutable_min_value = e.min
      this.mutable_max_value = e.max
      $("#" + this.slider_name).slider('values',0, e.min);
      $("#" + this.slider_name).slider('values',1, e.max);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
