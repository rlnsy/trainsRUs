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
      <label for="input-1">First Name</label>
      <b-form-input
        id="input-1"
        v-model="form.firstName"
        :state="inputValidation.firstName"
      />
      <label for="input-2">Last Name</label>
      <b-form-input
        id="input-2"
        v-model="form.lastName"
        :state="inputValidation.lastName"
      />
      <label for="input-3">Phone Number</label>
      <b-form-input
        id="input-3"
        v-model="form.phoneNumber"
        :state="inputValidation.phoneNumber"
      />
      <label for="input-4">Job Title</label>
      <b-form-input
        id="input-4"
        v-model="form.role"
        :state="inputValidation.role"
      />
      <label for="input-5">Department</label>
      <b-form-select
        id="input-5"
        v-model="form.workerType"
        :options="departments"
        :state="inputValidation.workerType"
      />
      <label for="input-6">Availabilty</label>
      <b-form-checkbox-group
        v-model="form.checked"
        :state="inputValidation.checked"
        id="input-6"
      >
        <b-form-checkbox value="Sa">
          Saturday
        </b-form-checkbox>
        <b-form-checkbox value="M">
          Monday
        </b-form-checkbox>
        <b-form-checkbox value="T">
          Tuesday
        </b-form-checkbox>
        <b-form-checkbox value="W">
          Wednesday
        </b-form-checkbox>
        <b-form-checkbox value="Th">
          Thursday
        </b-form-checkbox>
        <b-form-checkbox value="F">
          Friday
        </b-form-checkbox>
        <b-form-checkbox value="S">
          Sunday
        </b-form-checkbox>
      </b-form-checkbox-group>
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
import { Departments, goodStatusCode } from '../../utils/constants.js'
import workerCalls from '../../utils/workerCalls.js'

export default {
  name: 'AddWorkerForm',
  data() {
      return {
        form: {
          firstName: '',
          lastName: '',
          phoneNumber: '',
          role: '',
          workerType: '',
          checked: []
        },
        inputValidation: {
          firstName: null,
          lastName: null,
          phoneNumber: null,
          role: null,
          workerType: null,
          checked: null
        },
        departments: Object.values(Departments),
        showDismissibleAlert: false,
        alertText: '',
        alertType: ''
      }
  },
  methods: {
      async onSubmit() {
        if(this.validateForm()){
            var reducer = (acc, curr) => acc !== "" ? acc + " " + curr : curr;
            const postForm = {
                firstName: this.form.firstName,
                lastName: this.form.lastName,
                phoneNumber: this.form.phoneNumber,
                role: this.form.role,
                workerType: this.form.workerType,
                availability: this.form.checked.reduce(reducer, "")
            }

            try {
              const response = await workerCalls.createWorker(postForm)
              if(goodStatusCode(response.status)){ 
                this.alertText = "Worker Created"
                this.alertType = "success"
                this.showDismissibleAlert = true;
              } else {
                this.alertText = "Creation Failed"
                this.alertType = "danger"
                this.showDismissibleAlert = true;
              }
            } catch (error) {
              this.alertText = error
              this.alertType = "danger"
              this.showDismissibleAlert = true;
            }
            
            this.form = {
                firstName: '',
                lastName: '',
                phoneNumber: '',
                role: '',
                workerType: '',
                checked: []
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
          if (typeof this.form.firstName !== 'string' || !this.form.firstName instanceof String || this.form.firstName === ''){
              this.inputValidation.firstName = false;
              valid = false;
          } else {
              this.inputValidation.firstName = null;
          }
          if (typeof this.form.lastName !== 'string' || !this.form.lastName instanceof String || this.form.lastName === ''){
              this.inputValidation.lastName = false;
              valid = false;
          } else {
              this.inputValidation.lastName = null;
          }
          if (typeof this.form.phoneNumber !== 'string' || !this.form.phoneNumber instanceof String || this.form.phoneNumber === ''){
              this.inputValidation.phoneNumber = false;
              valid = false;
          } else {
              this.inputValidation.phoneNumber = null;
          }
          if (typeof this.form.role !== 'string' || !this.form.role instanceof String || this.form.role === ''){
              this.inputValidation.role = false;
              valid = false;
          } else {
              this.inputValidation.role = null;
          }
          if (typeof this.form.workerType !== 'string' || !this.form.workerType instanceof String || this.form.workerType === ''){
              this.inputValidation.workerType = false;
              valid = false;
          } else {
              this.inputValidation.workerType = null;
          }
          if (this.form.checked === []){
              this.inputValidation.checked = false;
              valid = false;
          } else {
              this.inputValidation.checked = null;
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
