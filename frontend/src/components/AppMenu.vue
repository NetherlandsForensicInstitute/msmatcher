<template>
  <div class="col-md-2">
    <form>
      <div class="form-group">
        <label for="base_selection">Experiment</label>
        <select class="form-control" id="base_selection" v-model="base_selected">
          <option v-bind:value="-1">select item</option>
          <option v-for="ex in experiments" v-bind:value="ex.id">{{ex.name}}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="compare_selection">Reference</label>
        <select class="form-control" id="compare_selection" v-model="compare_selected">
          <option v-bind:value="-1">select item</option>
          <option v-for="ex in experiments" v-bind:value="ex.id">{{ex.name}}</option>
        </select>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props : ["experiments"],
  data () {
    return {
      "base_selected": -1,
      "compare_selected": -1
    }
  },
  watch: {
    base_selected : function(e) {
      this.$emit('base_selected', this.base_selected)
    },
    compare_selected : function(e) {
      this.$emit('compare_selected', this.compare_selected)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
