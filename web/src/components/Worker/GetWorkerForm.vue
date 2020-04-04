<template>
  <div class="form-input-output">
    <label for="input-1">Worker ID</label>
    <b-form inline>
      <b-alert
        v-model="showDismissibleAlert"
        variant="danger"
        dismissible
      >
        {{ alertText }}
      </b-alert>
      <b-form-input
        id="input-1"
        v-model="form.id"
        :state="inputValidation.id"
      />
      <b-button
        @click="onSubmit"
        variant="primary"
      >
        Submit
      </b-button>
    </b-form>
    <b-card
      class="mt-3"
      header="Worker Info"
    >
      <pre class="m-0">{{ workerInfo }}</pre>
    </b-card>
  </div>
</template>

<script>

export default {
  name: 'GetWorkerForm',
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
        workerInfo: {}
      }
  },
  methods: {
      onSubmit() {
        if(this.validateForm()){
            console.log(JSON.stringify(this.form))
            this.form = {
                id: '',
            }
            // TODO: Set workerInfo Object based on response
        } else {
            this.alertText = "The following fields have issues: "
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
.form-input-output {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    > form > button {
        margin-left: 5px;
    }

    .card {
        width: 90%;
    }
}
</style>
