<template>
  <div class="form-input-output">
    <b-form>
      <b-alert
        v-model="showDismissibleAlert"
        variant="danger"
        dismissible
      >
        {{ alertText }}
      </b-alert>
      <label for="input-1">Ticket ID</label>
      <b-form-input
        id="input-1"
        v-model="form.ticketID"
        :state="inputValidation.ticketID"
      />
      <label for="input-2">Trip ID</label>
      <b-form-input
        id="input-2"
        v-model="form.tripID"
        :state="inputValidation.tripID"
      />
      <b-button
        @click="onSubmit"
        variant="primary"
        style="align-self: flex-end"
      >
        Submit
      </b-button>
    </b-form>
    <b-card
      class="mt-3"
      header="Ticket Info"
      :border-variant="cardVariant"
      :header-bg-variant="cardVariant"
      :header-text-variant="cardVariant === 'normal' ? 'black' : 'white'"
    >
      <pre class="m-0">{{ ticketInfo }}</pre>
    </b-card>
  </div>
</template>

<script>
import trainCalls from '../../utils/trainCalls.js'

export default {
  name: 'CheckTicketForm',
  data() {
      return {
        form: {
          ticketID: '',
          tripID: '',
        },
        inputValidation: {
          ticketID: null,
          tripID: null,
        },
        showDismissibleAlert: false,
        alertText: '',
        ticketInfo: {},
        cardVariant: 'normal',
      }
  },
  methods: {
      async onSubmit() {
        if(this.validateForm()){
            console.log(JSON.stringify(this.form))
            this.ticketInfo = await trainCalls.getTicketInfo(JSON.stringify(this.form)) 
            cardVariant = this.ticketInfo.valid ? 'success' : 'danger'
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
          if (typeof this.form.ticketID !== 'string' || !this.form.ticketID instanceof String || this.form.ticketID === ''){
              this.inputValidation.ticketID = false;
              valid = false;
          } else {
              this.inputValidation.ticketID = null;
          } 
          if (typeof this.form.tripID !== 'string' || !this.form.tripID instanceof String || this.form.tripID === ''){
              this.inputValidation.tripID = false;
              valid = false;
          } else {
              this.inputValidation.tripID = null;
          }
          return valid
      }
  },
};
</script>

<style lang="scss" scoped>
form {
    display: flex;
    flex-direction: column;

    > input {
        margin-bottom: 10px;
    }
}

</style>