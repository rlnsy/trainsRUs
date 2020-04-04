<template>
  <div class="track">
    <b-modal
      id="modal-2"
      :title="this.currentFormHeader"
      hide-footer
    >
      <update-segment-form v-if="formIndex === 0" />
      <filter-table-form
        v-if="formIndex === 1"
        @submit="handleFilter"
      />
    </b-modal>
    <h2>Track Segment Maintenance</h2>
    <div class="l-row">
      <h4>Summary Stats</h4>
      <button @click="loadSummary()">
        Load
      </button>
    </div>
    <div class="summary">
      <div>
        <p class="stat">
          {{ summaryStats.totalTracks }}
        </p>
        <p>Track Segments</p>
      </div>
      <span />
      <div>
        <p
          class="stat"
          style="color: #FFBA7C;"
        >
          {{ summaryStats.needRepairs }}
        </p>
        <p>Need Repairs</p>
      </div>
      <span />
      <div>
        <p
          class="stat"
          style="color: #FF8989;"
        >
          {{ summaryStats.criticalCondition }}
        </p>
        <p>Critical Condition</p>
      </div>
    </div>
    <div
      class="l-row"
      style="margin-bottom: 20px;"
    >
      <h4>All Tracks</h4>
      <button @click="loadTable()">
        Load
      </button>
    </div>
    <b-table :items="this.tracks" />
    <div class="actions">
      <h4>Actions</h4>
      <a
        href="#"
        v-b-modal.modal-2
        @click="currentFormHeader='Update Track Segment'; formIndex = 0"
      >Update Track Segment</a>
      <a 
        href="#"
        v-b-modal.modal-2
        @click="currentFormHeader='Filter Table By Condition'; formIndex = 1"
      >Filter Table By Condition</a>
    </div>
  </div>
</template>

<script>
import trackCalls from '../../utils/trackCalls.js'
import UpdateSegmentForm from './UpdateSegmentForm.vue'
import FilterTableForm from './FilterTableForm.vue'

export default {
  name: 'Tracks',
  components: {
      UpdateSegmentForm,
      FilterTableForm,
  },
  data() {
    return {
      summaryStats: {
        totalTracks: 0,
        needRepairs: 0,
        criticalCondition: 0,
      },
      tracks: [],
      currentFormHeader: '',
      formIndex: 0,
      tableCondition: '',
    }
  },
  methods: {
      async loadSummary() {
          this.summaryStats = await trackCalls.getSummary()
      },
      async loadTable() {
          this.tracks =  await trackCalls.getAllTracks(this.tableCondition)
      },
      async handleFilter(evt) {
          this.tableCondition = evt
          await this.loadTable()
          this.$bvModal.hide('modal-2')
      },
  },
};
</script>

<style scoped lang="scss">
.track{
    position: relative;
    width: 100%;
    height: 100%;
    padding: 30px 50px;
}

button{
    font-size: 100%;
    font-family: inherit;
    border: 0;
    padding: 0;
    width: 55px;
    height: 2em;
    margin-left: 15px;
    border-radius: 5px;
    background-color: var(--trainBlue);
    color: white;
}

.summary{
    padding-left: 5vw;
    display: flex;
    align-items: center;
    padding-top: 20px;

    > div {
        display: flex;
        flex-direction: column;
        align-items: center;

        > .stat {
            font-size: 72px;
            font-weight: bold;
        }

        > p {
            font-size : 18px;
        }
    }

    > span {
        margin: 0 50px;
        width: 2px;
        background-color: lightgray;
        height: 120px;
    }
}

.l-row{
    margin-top: 30px;
    padding-left: 2em;
    display: flex;
    align-items: center;
}

.actions{
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    right: 70px;
    top: 30px;
}
</style>
