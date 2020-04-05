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
      <label for="input-1">Seat Number</label>
      <b-form-input
        id="input-1"
        v-model="form.seatNumber"
        :state="inputValidation.seatNumber"
        type="number"
      />
      <label for="input-2">Trip ID</label>
      <b-form-input
        id="input-2"
        v-model="form.tripID"
        :state="inputValidation.tripID"
        type="number"
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
          seatNumber: '',
          tripID: '',
        },
        inputValidation: {
          seatNumber: null,
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
            const postForm = {
              'tripId': Number(this.form.tripID),
              'seatNumber': Number(this.form.seatNumber)
            }
            try {
              this.ticketInfo = await trainCalls.getTicketInfo(postForm)
              this.cardVariant = 'success'
            } catch (error) {
              this.cardVariant = 'danger'
              this.alertText = error
              this.showDismissibleAlert = true;
            }
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
          if (typeof this.form.seatNumber !== 'string' || !this.form.seatNumber instanceof String || this.form.seatNumber === ''){
              this.inputValidation.seatNumber = false;
              valid = false;
          } else {
              this.inputValidation.seatNumber = null;
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