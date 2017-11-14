<template>
  <div>
    <div :id="name"></div>
  </div>
</template>

<script>
export default {
  props: [
    "name",
    "experiments_data"
  ],
  data () {
    return {
      "plot": null
    }
  },
  mounted () {
    this.plot = document.getElementById(this.name);
    Plotly.newPlot(this.plot, [[], []]);
  },
  watch: {
    experiments_data: function (e) {
      this.plotExperiments(this.plot, this.experiments_data, this.name)
    }
  },
  methods: {
    /**
     * Maps data of a single experiment to a plotly-plottable structure.
     *
     * @param experiment a single experiment ('data' property of API call result)
     * @param linecolor color of the line in the plot
     */
    mapExperimentDataToPlot: function(experimentData, linecolor, name) {
        var x_values = [];
        var y_values = [];
        var text_values = [];
        var annotations = [];

        var points = experimentData.points
        var key = 'mz' in points[0] ? 'mz' : 'rt';

        for(var i = 0; i < points.length -1; i++) {
            // create a spike, by adding: (x,0) (x,actual value) (null,null);
            var x = 'mz' in points[i] ? points[i].mz : points[i].rt
            var y = points[i].intensity;
            var formulas = points[i].formulas ? points[i].formulas : "?";
            var names = points[i].names ? points[i].names : "?";
            var hover =
              key + ": " + x + "<br />" +
              "Intensity: " + y + "<br />" +
              "Formulas: " + formulas + "<br />" +
              "Names: " + names;

            x_values.push(x);
            y_values.push(0);
            x_values.push(x);
            y_values.push(y);
            x_values.push(null);
            y_values.push(null);

            text_values.push("");
            text_values.push(hover);
            text_values.push("");
            annotations.push(this.createAnnotation(x, y, formulas, linecolor));
        }
        return {
            x: x_values,
            y: y_values,
            text: text_values,
            name: name,
            mode: 'lines',
            connectgaps: false,
            hoverinfo: 'text',
            line: {'color': linecolor, 'width': 0.5},
            annotations: annotations,
        };
    },


    /**
     * Crude local optimum detection
     */
    is_local_optimum: function(index, points) {
       var offset = 500; // TODO, what is a good value here, does this work well with filters?
       var x = points[index].x;
       var y = points[index].y;
       for(var j = index - 1; j > Math.max(0, index-offset); j--) {
          if(points[j].y > y) {
            return false;
          }
       }
       for(var j = index + 1; j < Math.min(index+offset, points.length-1); j++) {
          if(points[j].y > y) {
            return false;
          }
       }
       return true;
    },

    createAnnotation: function(x, y, label, color) {
        return {
          x: x,
          y: y,
          text: label,
          xref: 'x',
          yref: 'y',
          arrowcolor: color,
          arrowhead: 2,
          font: {color: color}
        }
    },

    /**
     * Method that plots peaks for multiple experiments.
     *
     * @param location id of html element where to plot
     * @param experiment list of experiments
     * @param label to put on x-asis
     */
    plotExperiments: function(location, experiments, x_label) {
        var experimentLineColors = ['#529AC6', '#FF9A42', 'red', 'black'];

        // determine intensity upperbound for all experiments
        // set an annotation threshold: annotate peaks where intensity > mean
        var intensity_max = 0;
        var xval = this.xval;
        for(var l = 0; l < experiments.length; l++) {
            intensity_max = experiments[l].points.reduce(function(a,b){return Math.max(a, b.intensity);}, intensity_max);
        }

        // map experiments to a plotly structure, traditional loop to get index for line color
        var experimentsPlotly = [];
        var annotations = [];
        for(var l = 0; l < experiments.length; l++) {
            var experiment = this.mapExperimentDataToPlot(experiments[l], experimentLineColors[l], l == 0 ? "Experiment" : "Reference");
            experimentsPlotly.push(experiment);
            annotations = annotations.concat(experiment.annotations);
        }

        // apply a strategy to remove all non-local optima
        annotations.sort((a,b) => a.x - b.x);
        var displayed_annotations = [];
        for(var i = 0; i < annotations.length; i++) {
            var annotation = annotations[i];
            if(annotation.y > (intensity_max / 4) && this.is_local_optimum(i, annotations)) {
              displayed_annotations.push(annotation);
            }
        }

        var layout = {
            xaxis: {title: x_label, rangemode: 'tozero', autorange:true},
            yaxis: {title: 'intensity', rangemode: 'tozero', autorange:true},
            height: 300,
            showlegend: true,
            legend: {"orientation": "h"},
            annotations: displayed_annotations
        };

        // purge before newPlot
        Plotly.purge(location);
        Plotly.newPlot(location, experimentsPlotly, layout);
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
