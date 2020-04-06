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
      <label for="input-1">Select Table Columns to Display</label>
      <b-form-checkbox-group
        v-model="form.checked"
        :state="inputValidation.checked"
        :options="allColumns"
        id="input-1"
        switches
        stacked
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
import workerCalls from '../../utils/workerCalls';

export default {
  name: 'TableColumnForm',
  props: {
      currentColumns: {
          type: Array,
          default: () => {
              return []
          }
      },
  },
  data() {
      return {
        form: {
          checked: this.currentColumns,
        },
        inputValidation: {
          checked: null,
        },
        allColumns: [],
        showDismissibleAlert: false,
        alertText: '',
        alertType: ''
      }
  },
  async mounted() {
      this.allColumns = await workerCalls.getColumns()
  },
  methods: {
      onSubmit() {
        if(this.validateForm()){
            this.$emit('submit', this.form.checked)
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
          if(typeof this.form.checked.length === 0){
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
    margin-left: 10%;
    > button {
        margin-top: 15px;
        align-self: flex-end;
    }
}

</style>
