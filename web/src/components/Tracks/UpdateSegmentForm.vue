<template>
  <div>
    <b-form>
      <b-alert
        v-model="showDismissibleAlert"
        :variant="alertType"
        dismissible
      >
        {{ alertText }}
      </b-alert>
      <label for="input-1">Segment ID</label>
      <b-form-input
        id="input-1"
        v-model="form.id"
        :state="inputValidation.id"
        type="number"
      />
      <label for="input-2">New Length (Optional)</label>
      <b-form-input
        id="input-2"
        v-model="form.length"
        :state="inputValidation.length"
        type="number"
      />
      <label for="input-3">New Condition (Optional)</label>
      <b-form-select
        id="input-3"
        v-model="form.condition"
        :options="conditions"
        :state="inputValidation.condition"
      />
      <label for="input-4">New Start Station (Optional)</label>
      <b-form-select
        id="input-4"
        v-model="form.startStation"
        :options="stations"
        :state="inputValidation.startStation"
      />
      <label for="input-5">New End Station (Optional)</label>
      <b-form-select
        id="input-5"
        v-model="form.endStation"
        :options="stations"
        :state="inputValidation.endStation"
      />
      <b-button
        @click="onSubmit"
        variant="primary"
      >
        Submit
      </b-button>
    </b-form>
  </div>
</template>

<script>
import { Conditions } from '../../utils/constants.js'
import stationCalls from '../../utils/stationCalls.js'
import trackCalls from '../../utils/trackCalls.js'
import { goodStatusCode } from '../../utils/constants.js'

export default {
  name: 'UpdateSegmentForm',
  data() {
      return {
        form: {
          id: '',
          length: '',
          condition: '',
          startStation: '',
          endStation: '',
        },
        inputValidation: {
          id: null,
          length: null,
          condition: null,
          startStation: null,
          endStation: null,
        },
        conditions: Object.values(Conditions),
        stations: [],
        showDismissibleAlert: false,
        alertText: '',
        alertType: ''
      }
  },
  async mounted(){
    var response = await stationCalls.getAllStations()
    this.stations = response.data.map(s => s.sname)
  },
  methods: {
      async onSubmit() {
        if(this.validateForm()){
            var postForm = {}
            for(var key in this.form){
                if(this.form[key] !== ''){
                    switch(key){
                      case 'condition': 
                        postForm.status = this.form.condition
                        break;
                      case 'length': 
                        postForm.length = Number(this.form.length)
                        break;
                      case 'id':
                        postForm.segmentId = Number(this.form.id)
                        break;
                      default:
                        postForm[key] = this.form[key]
                        break;
                    }
                }
            }

            try {
              const response = await trackCalls.updateSegment(postForm)
              if(goodStatusCode(response.status)){ 
                this.alertText = "Segment Updated"
                this.alertType = "success"
                this.showDismissibleAlert = true;
              } else {
                this.alertText = response.message
                this.alertType = "danger"
                this.showDismissibleAlert = true;
              }
            } catch (error) {
              this.alertText = error
              this.alertType = "danger"
              this.showDismissibleAlert = true;
            }
    
            this.form = {
                id: '',
                length: '',
                condition: '',
                startStation: '',
                endStation: '',
            }
        } else {
            this.alertText = "The following fields have issues: "
            this.alertType = "danger"
            for(var input in this.inputValidation){
                this.inputValidation[input] === false ? this.alertText = this.alertText + ' ' + input : ''
            }
            this.showDismissibleAlert = true;
        }
      },
      validateForm() {
          var valid = true
          if(typeof this.form.id !== 'string' || !this.form.id instanceof String || this.form.id === ''){
              this.inputValidation.id = false;
              valid = false;
          } else {
              this.inputValidation.id = null;
          }
          if(isNaN(this.form.length)){
              this.inputValidation.length = false;
              valid = false;
          } else {
              this.inputValidation.length = null;
          }
          if(typeof this.form.condition !== 'string' || !this.form.condition instanceof String){
              this.inputValidation.condition = false;
              valid = false;
          } else {
              this.inputValidation.condition = null;
          }
          if(typeof this.form.startStation !== 'string' || !this.form.startStation instanceof String){
              this.inputValidation.startStation = false;
              valid = false;
          } else {
              this.inputValidation.startStation = null;
          }
          if(typeof this.form.endStation !== 'string' || !this.form.endStation instanceof String){
              this.inputValidation.endStation = false;
              valid = false;
          } else {
              this.inputValidation.endStation = null;
          }
          if(this.form.startStation === this.form.endStation && this.form.startStation !== ''){
            this.inputValidation.startStation = false;
            this.inputValidation.endStation = false;
            valid = false;
          }
          return valid
      }
  },
};
</script>

<style scoped lang="scss">

form {
    display: flex;
    flex-direction: column;

    > label {
        margin-top: 7px;
    }

    > button {
        margin-top: 15px;
        align-self: flex-end;
    }
}

</style>
