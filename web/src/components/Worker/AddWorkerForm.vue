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
      <label for="input-3">Phone Number (No Formatting)</label>
      <b-form-input
        id="input-3"
        v-model="form.phoneNumber"
        :state="inputValidation.phoneNumber"
        type="number"
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
        v-model="form.type"
        :options="departments"
        :state="inputValidation.type"
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
import { Departments } from '../../utils/constants.js'

export default {
  name: 'AddWorkerForm',
  data() {
      return {
        form: {
          firstName: '',
          lastName: '',
          phoneNumber: '',
          role: '',
          type: '',
          checked: []
        },
        inputValidation: {
          firstName: null,
          lastName: null,
          phoneNumber: null,
          role: null,
          type: null,
          checked: null
        },
        departments: [{ text: 'Select One', value: null }].concat(Object.values(Departments)),
        showDismissibleAlert: false,
        alertText: '',
        alertType: ''
      }
  },
  methods: {
      onSubmit() {
        if(this.validateForm()){
            var reducer = (acc, curr) => acc !== "" ? acc + " " + curr : curr;
            const postForm = {
                firstName: this.form.firstName,
                lastName: this.form.lastName,
                phoneNumber: this.form.phoneNumber,
                role: this.form.role,
                type: this.form.type,
                availabilty: this.form.checked.reduce(reducer, "")
            }

            // TODO: Send postForm to creation endpoint and verify success
            console.log(JSON.stringify(postForm))

            
            this.alertText = "Worker Created"
            this.alertType = "success"
            this.showDismissibleAlert = true;

            this.form = {
                firstName: '',
                lastName: '',
                phoneNumber: '',
                role: '',
                type: '',
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
          if (this.form.phoneNumber === ''){
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
          if (typeof this.form.type !== 'string' || !this.form.type instanceof String || this.form.type === ''){
              this.inputValidation.type = false;
              valid = false;
          } else {
              this.inputValidation.type = null;
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
