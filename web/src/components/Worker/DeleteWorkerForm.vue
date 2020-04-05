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
      <label for="input-1">Worker ID</label>
      <b-form-input
        id="input-1"
        v-model="form.id"
        :state="inputValidation.id"
        type="number"
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
import workerCalls from '../../utils/workerCalls.js'

export default {
  name: 'DeleteWorkerForm',
  data() {
      return {
        form: {
          id: '',
        },
        inputValidation: {
          id: null
        },
        showDismissibleAlert: false,
        alertText: '',
        alertType: ''
      }
  },
  methods: {
      async onSubmit() {
        if(this.validateForm()){
            var postForm = {
              'workerId': Number(this.form.id),
            }
            try {
              const response = await workerCalls.deleteWorker(postForm)
              this.form = {
                id: '',
              }
              if(response.message === 'success'){ 
                this.alertText = "Worker Deleted"
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
          if (typeof this.form.id !== 'string' || !this.form.id instanceof String || this.form.id === ''){
              this.inputValidation.id = false;
              valid = false;
          } else {
              this.inputValidation.id = null;
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
