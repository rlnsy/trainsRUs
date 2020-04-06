<template>
  <div class="worker">
    <b-modal
      id="modal-1"
      :title="this.currentFormHeader"
      hide-footer
    >
      <add-worker-form v-if="formIndex === 0" />
      <delete-worker-form v-if="formIndex === 1" />
      <get-worker-form v-if="formIndex === 2" />
      <table-column-form v-if="formIndex === 3" @submit="handleFilter" :currentColumns="tableColumns"/>
    </b-modal>
    <h2>Manage All Workers</h2>
    <div class="l-row">
      <h4>Summary Stats</h4>
      <button @click="loadSummary()">
        Reload
      </button>
    </div>
    <div class="summary">
      <div>
        <p class="stat">
          {{ summaryStats.totalWorkers }}
        </p>
        <p>Total Workers</p>
      </div>
      <span />
      <div>
        <p
          class="stat"
          style="color: var(--trainAccentBlue);"
        >
          {{ summaryStats.workingToday }}
        </p>
        <p>Working Today</p>
      </div>
    </div>
    <div
      class="l-row"
      style="margin-bottom: 20px;"
    >
      <h4>All Workers</h4>
      <button @click="loadTable()">
        Reload
      </button>
    </div>
    <b-table :items="this.workers" />
    <div class="actions">
      <h4>Actions</h4>
      <a
        href="#"
        v-b-modal.modal-1
        @click="currentFormHeader='Add New Worker'; formIndex = 0"
      >Add New Worker</a>
      <a 
        href="#"
        v-b-modal.modal-1
        @click="currentFormHeader='Delete Worker'; formIndex = 1"
      >Delete Worker</a>
      <a
        href="#"
        v-b-modal.modal-1
        @click="currentFormHeader='Get Worker'; formIndex = 2"
      >
        Get Worker</a>
      <a
        href="#"
        v-b-modal.modal-1
        @click="currentFormHeader='Choose Columns'; formIndex = 3"
      >
        Choose Table Columns</a>
    </div>
  </div>
</template>

<script>
import workerCalls from '../../utils/workerCalls.js'
import AddWorkerForm from './AddWorkerForm.vue'
import DeleteWorkerForm from './DeleteWorkerForm.vue'
import GetWorkerForm from './GetWorkerForm.vue'
import TableColumnForm from './TableColumnForm.vue' 

export default {
  name: 'Workers',
  components: {
      AddWorkerForm,
      DeleteWorkerForm,
      GetWorkerForm,
      TableColumnForm,
  },
  data() {
    return {
      summaryStats: {
        totalWorkers: 0,
        workingToday: 0,
      },
      workers: [],
      currentFormHeader: '',
      formIndex: 0,
      tableColumns: [],
    }
  },
  async mounted() {
    this.tableColumns = await workerCalls.getColumns()
    this.loadSummary()
    this.loadTable() 
  },
  methods: {
      async loadSummary() {
          this.summaryStats = await workerCalls.getSummary()
      },
      async loadTable() {
          const response = await workerCalls.getAllWorkers(this.tableColumns)
          this.workers = response.data
      },
      async handleFilter(evt) {
          this.tableColumns = evt
          await this.loadTable()
          this.$bvModal.hide('modal-1')
      },
  },
};
</script>

<style scoped lang="scss">
.worker{
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
