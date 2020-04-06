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
      <table-column-form
        v-if="formIndex === 3"
        @submit="handleFilter"
        :current-columns="tableColumns"
      />
      <div v-if="formIndex === 4">
        <p>A maintenance worker is considered overworked if they are responsible for every track in the system</p>
        <b-card header="Overworked Employee Ids">
          {{ overworked }}
        </b-card>
      </div>
    </b-modal>
    <h2>Manage All Workers</h2>
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
        v-if="loaded"
        class="summary"
      >
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
        <span />
        <div>
          <p
            class="stat"
            style="color: #FF8989;"
          >
            {{ overworked.length }}
          </p>
          <p
            class="fakeLink text-center"
            v-b-modal.modal-1
            @click="currentFormHeader='Overworked Worker List'; formIndex = 4"
          >
            Overworked Track Workers
          </p>
        </div>
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
      <a
        href="#"
        v-b-modal.modal-1
        @click="currentFormHeader='Choose Columns'; formIndex = 3"
        style="margin-left: 20px;"
      >
        Choose Table Columns</a>
    </div>
    <b-table
      :items="this.workers"
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
      overworked: [],
      loadingProgress: {
        table: false,
        summary: false,
      },
    }
  },
  computed: {
    loaded(){
      for(let [key, value] of Object.entries(this.loadingProgress)){
        if(value == false){
          return false
        }
      }
      return true
    }
  },
  async mounted() {
    this.tableColumns = await workerCalls.getColumns()
    await this.loadSummary().then(r => {
      this.loadingProgress.summary = true;
    })
    await this.loadTable().then(r => {
      this.loadingProgress.table = true;
    })
  },
  methods: {
      async loadSummary() {
          this.summaryStats = await workerCalls.getSummary()
          const response = await workerCalls.getOverworked()
          this.overworked = response.data
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
    height: 35px;
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
        height: 100%;

        > .stat {
            font-size: 72px;
            font-weight: bold;
        }

        > .fakeLink{
          color: var(--trainBlue);
        }

        > .fakeLink:hover{
            color: #3649ff;
            text-decoration: underline;
            cursor: pointer;
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
</style>
