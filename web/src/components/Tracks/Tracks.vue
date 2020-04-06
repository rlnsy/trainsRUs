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
    <b-alert
      v-model="showDismissibleAlert"
      variant="danger"
      dismissible
      style="max-width: 50vw;"
    >
      {{ alertText }}
    </b-alert>
    <h2>Track Segment Maintenance</h2>
    <div class="l-row">
      <h4>Summary Stats</h4>
      <button @click="loadSummary()">
        Reload
      </button>
    </div>
    <div>
      <div
        v-if="!loaded"
        class="text-center"
        style="color: var(--trainBlue); margin-top: 15px; height: 100px; display:flex; align-items:center; margin-left: 20vw;"
      >
        <b-spinner
          class="align-middle"
          style="margin-right: 15px"
        />
        <strong> Loading...</strong>
      </div>
      <div
        class="summary"
        v-if="loaded"
      >
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
        <span />
        <div>
          <p
            class="stat"
          >
            {{ summaryStats.avergeTripLength }}
          </p>
          <p>Average # of Segments Per Trip</p>
        </div>
      </div>
    </div>
    <div
      class="l-row"
      style="margin-bottom: 20px;"
    >
      <h4>All Tracks</h4>
      <button @click="loadTable()">
        Reload
      </button>
    </div>
    <b-table
      :items="this.tracks"
      :busy="!loaded"
    >
      <template v-slot:table-busy>
        <div
          class="text-center"
          style="color: var(--trainBlue); margin-top: 15px;"
        >
          <b-spinner class="align-middle" />
          <strong> Loading...</strong>
        </div>
      </template>
    </b-table>
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
        avergeTripLength: 0,
      },
      tracks: [],
      currentFormHeader: '',
      formIndex: 0,
      tableCondition: '',
      showDismissibleAlert: false,
      alertText: '',
      loadingProgress: {
        table: false,
        summary: false
      },
    }
  },
  computed: {
    loaded(){
      for(let [key, value] of Object.entries(this.loadingProgress)){
        console.log(key)
        if(value == false){
          return false
        }
      }
      return true
    }
  },
  async mounted(){
    await this.loadSummary().then(
            r => this.loadingProgress.summary = true
          )
    await this.loadTable().then(
            r => this.loadingProgress.table = true
          )
  },
  methods: {
      async loadSummary() {
        try {
          this.summaryStats = await trackCalls.getSummary()
        } catch (error) {
          this.alertText = error
          this.showDismissibleAlert = true
        }
      },
      async loadTable() {
        try {
          const response = await trackCalls.getAllTracks(this.tableCondition)
          this.tracks = response.data
        } catch (error) {
          this.alertText = error
          this.showDismissibleAlert = true
        }
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
    overflow-x: hidden;
    overflow-y: auto;
}

button{
    font-size: 100%;
    font-family: inherit;
    border: 0;
    padding: 0;
    width: 75px;
    height: 35px;
    margin-left: 15px;
    border-radius: 5px;
    background-color: var(--trainBlue);
    color: white;
}

button:active{
  -webkit-box-shadow: inset 0px 0px 5px #4f60ff;
     -moz-box-shadow: inset 0px 0px 5px #4f60ff;
          box-shadow: inset 0px 0px 5px #4f60ff;
  filter: brightness(90%);
}

button:hover {
    color: #fff;
    background-color: #5c6bff;
    border-color: #4f60ff;
    text-decoration: none;
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
