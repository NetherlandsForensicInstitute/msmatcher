<template>
  <div class="col-md-5">
    <div id="placeholder_surface_plot"></div>
  </div>
</template>

<script>
  export default {
    props: [
      "data"
    ],
    data () {
      return {
        "layout": {
          height: 800,
          margin: {t: 0},
          paper_bgcolor: 'rgba(0,0,0,0)',
          autosize: true,
          scene: {
            xaxis: {title: 'rt'},
            yaxis: {title: 'm/z'},
            zaxis: {title: 'intensity'}
          }
        },
        "location": null,
        "selectedRt": -1.0,
        "selectedMz": -1.0
      }
    },
    mounted () {
      this.location = document.getElementById("placeholder_surface_plot")
      Plotly.newPlot(this.location, [{z: [[0, 0]], type: 'surface'}], this.layout)
    },
    methods: {
      set_ticks: function (values, right_axis) {
        // round the labels
        values.forEach(function (x, index, arr) {
          arr[index] = Math.round(x * 100) / 100
        });
        // label the first, last and middle value of the x and y axes
        right_axis.ticktext = [values[0], values[Math.round((values.length - 1) / 2)], values[values.length - 1]]
        right_axis.tickvals = [0, values.length / 2, values.length]
      },
      build3dgraph: function () {
        Plotly.purge(this.location)

        this.set_ticks(this.data.meta_data.rt_min_values, this.layout.scene.xaxis);
        this.set_ticks(this.data.meta_data.mz_min_values, this.layout.scene.yaxis);

        /*
         builds a 3d surface plot and adds it to the template
         */
        Plotly.newPlot(this.location, [this.data.graph_data], this.layout);

        // add an on click event listener to the 3d plot
        this.location.on('plotly_click', function (selection) {
          var rt_lower, rt_upper, mz_lower, mz_upper;

          this.selectedRt = selection.points[0].x
          this.selectedMz = selection.points[0].y

          // retreive the bucket values from the matrix
          rt_lower = this.data.meta_data.rt_min_values[selection.points[0].x];
          rt_upper = rt_lower + this.data.meta_data.rt_bin_size;

          mz_lower = this.data.meta_data.mz_min_values[selection.points[0].y];
          mz_upper = mz_lower + this.data.meta_data.mz_bin_size;
          // sends data back to the parent component
          this.$emit('rt_mz_selection_change', {
            rt_lower: rt_lower,
            rt_upper: rt_upper,
            mz_lower: mz_lower,
            mz_upper: mz_upper
          });
        }.bind(this))
      }
    },
    watch: {
      data: function (e) {
        this.build3dgraph()
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
