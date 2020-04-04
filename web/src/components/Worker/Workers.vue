<template>
  <div class="worker">
    <b-modal
      id="modal-1"
      :title="this.currentFormHeader"
      hide-footer
    >
      <add-worker-form @submit="$bvModal.hide('modal-1')" />
    </b-modal>
    <h2>Manage All Workers</h2>
    <div class="l-row">
      <h4>Summary Stats</h4>
      <button @click="loadSummary()">
        Load
      </button>
    </div>
    <div class="summary">
      <div>
        <p class="stat">
          {{ totalWorkers }}
        </p>
        <p>Total Workers</p>
      </div>
      <span />
      <div>
        <p
          class="stat"
          style="color: var(--trainAccentBlue);"
        >
          {{ workingToday }}
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
        Load
      </button>
    </div>
    <b-table :items="this.workers" />
    <div class="actions">
      <h4>Actions</h4>
      <a
        href="#"
        v-b-modal.modal-1
        @click="currentFormHeader='Add New Worker'; "
      >Add New Worker</a>
      <a href="#">Delete Worker</a>
      <a href="#">Get Worker</a>
      <a href="#">Change Table Rows</a>
    </div>
  </div>
</template>

<script>
import workerCalls from '../../utils/workerCalls.js'
import AddWorkerForm from './AddWorkerForm.vue'

export default {
  name: 'Workers',
  components: {
      AddWorkerForm,
  },
  data() {
    return {
      totalWorkers: 0,
      workingToday: 0,
      workers: [],
      currentFormHeader: '',
      formIndex: 0,
    }
  },
  methods: {
      async loadSummary() {
          var summary = await workerCalls.getSummary()
          this.totalWorkers = summary.totalWorkers
          this.workingToday = summary.workingToday
      },
      async loadTable() {
          var tableRows = await workerCalls.getAllWorkers()
          this.workers = tableRows
      }
  },
};
</script>

<style scoped lang="scss">
.worker{
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
    padding-left: 10vw;
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
        margin: 0 25px;
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
