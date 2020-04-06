<template>
  <div class="track">
    <b-modal
      id="modal-3"
      :title="this.currentFormHeader"
      hide-footer
    >
      <check-ticket-form />
    </b-modal>
    <b-alert
      v-model="showDismissibleAlert"
      variant="danger"
      dismissible
      style="max-width: 50vw;"
    >
      {{ alertText }}
    </b-alert>
    <h2>Train Worker Information</h2>
    <label for="input-1">Train Worker ID:</label>
    <b-form inline>
      <b-form-input
        id="input-1"
        v-model="id"
      />
      <b-button
        @click="onSubmit"
        variant="primary"
      >
        Get Shifts
      </b-button>
    </b-form>
    <div
      class="l-row"
      v-if="!statsIsEmpty"
    >
      <h4>Summary Stats</h4>
    </div>
    <div
      class="summary"
      v-if="!statsIsEmpty"
    >
      <div>
        <p class="stat">
          {{ summaryStats.upcomingShifts }}
        </p>
        <p>Upcoming Shifts</p>
      </div>
      <span />
      <div>
        <p
          class="stat"
          style="color: var(--trainAccentBlue);"
        >
          {{ summaryStats.distinctTrips }}
        </p>
        <p>Distinct Trips</p>
      </div>
    </div>
    <div
      class="l-row"
      v-if="shifts.length"
      style="margin-bottom: 20px"
    >
      <h4>Upcoming Shifts</h4>
    </div>
    <b-table :items="this.shifts" />
    <div class="actions">
      <h4>Actions</h4>
      <a
        href="#"
        v-b-modal.modal-3
        @click="currentFormHeader='Check Ticket'; formIndex = 0"
      >Check Tickets</a>
    </div>
  </div>
</template>

<script>
import trainCalls from '../../utils/trainCalls.js'
import CheckTicketForm from './CheckTicketsForm.vue'
import workerCalls from '../../utils/workerCalls';
import { goodStatusCode, Departments } from '../../utils/constants';

export default {
  name: 'Train',
  components: {
      CheckTicketForm,
  },
  data() {
    return {
      summaryStats: {},
      shifts: [],
      currentFormHeader: '',
      tableCondition: '',
      id: '',
      showDismissibleAlert: false,
      alertText: '',
    }
  },
  computed: {
      statsIsEmpty() {
        return Object.keys(this.summaryStats).length === 0;
      },
  },
  methods: {
      async loadSummary() {
        try{
          this.summaryStats = await trainCalls.getSummary(this.id)
        } catch(error) {
          this.displayError(error)
        }
      },
      async loadTable() {
        try {
          const response = await trainCalls.getShifts(this.id)
          this.shifts = response.data
        } catch(error) {
          this.displayError(error)
        }
      },
      async onSubmit() {
          if(this.id === ''){
              this.displayError("Please enter a value for ID")
              return;
          }
          var workerRes
          try {
            workerRes = await workerCalls.getWorker({'workerId': Number(this.id)})
          } catch (error) {
            this.displayError(error)
          }

          if(goodStatusCode(workerRes.status)){
            if(workerRes.data.workerType === Departments.TRAIN){
              this.loadTable()
              this.loadSummary()
              this.showDismissibleAlert = false;
            } else {
              this.displayError('Worker is not in Train Department')
            }
          } else {
            this.displayError(workerRes.data.message)
          }
          
      },
      displayError(msg){
          this.alertText = msg
          this.showDismissibleAlert = true
          this.resetPage()
      },
      resetPage(){
        this.shifts = []
        this.id = ''
        this.summaryStats = {}
      }
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

label{
    padding-left: 5vw;
    margin-top: 30px;
    font-size: 18px;
    font-weight: 700;
}

form{
    padding-left: 5vw;
}

button {
    margin-left: 15px;
    min-height: 35px;
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

button{
  color: white;
}
</style>
