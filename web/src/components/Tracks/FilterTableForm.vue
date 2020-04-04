<template>
  <div>
    <b-alert
      v-model="showDismissibleAlert"
      :variant="alertType"
      dismissible
    >
      {{ alertText }}
    </b-alert>
    <b-form>
      <h5>Keep rows where condition is:</h5>
      <b-form-select
        id="input-3"
        v-model="form.condition"
        :options="conditions"
        :state="inputValidation.condition"
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

export default {
  name: 'FilterTableForm',
  data() {
      return {
        form: {
          condition: '',
        },
        inputValidation: {
          condition: null,
        },
        conditions: Object.values(Conditions),
        showDismissibleAlert: false,
        alertText: '',
        alertType: ''
      }
  },
  methods: {
      onSubmit() {
        if(this.validateForm()){
            // TODO: Send form to GET endpoint and verify success
            console.log(JSON.stringify(this.form))

            // if successful:            
            this.alertText = "Call Successful"
            this.alertType = "success"
            this.showDismissibleAlert = true;

            this.$emit('submit', this.form.condition)

            this.form = {
                condition: '',
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
          if(typeof this.form.condition !== 'string' || !this.form.condition instanceof String){
              this.inputValidation.condition = false;
              valid = false;
          } else {
              this.inputValidation.condition = null;
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
