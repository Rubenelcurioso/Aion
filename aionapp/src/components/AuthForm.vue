<template>
    <div class="auth-form">
      <h1 class="text-h3 text-center">{{ title }}</h1>
      <h2 class="text-h5 text-center q-mb-md">{{ subtitle }}</h2>
      
      <q-card class="bg-third">
        <q-card-section>
          <q-form @submit="onSubmit" class="q-gutter-md" ref="formRef" autocorrect="off"
          autocapitalize="off"
          autocomplete="off"
          spellcheck="false"
          >
            <q-input
              v-for="field in fields"
              :key="field.name"
              v-model="formData[field.name]"
              :label="field.label"
              :type="field.type || 'text'"
              :rules="field.name === 'confirmPassword' ? [
                ...field.rules,
                val => val === formData.password || 'Passwords do not match'
              ] : field.rules"
              filled
            />
            <div class="text-center">
              <q-btn unelevated color="dark" :label="submitLabel" type="submit" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>    </div>
  </template>

  <script>
  import { ref, reactive } from 'vue'

  export default {
    name: 'AuthForm',
    props: {
      title: {
        type: String,
        required: true
      },
      subtitle: {
        type: String,
        required: true
      },
      fields: {
        type: Array,
        required: true
      },
      submitLabel: {
        type: String,
        default: 'Submit'
      }
    },
    emits: ['submit'],
    setup(props, { emit }) {
      const formRef = ref(null)
      const formData = reactive({})

      // Initialize formData with empty strings for each field
      props.fields.forEach(field => {
        formData[field.name] = ''
      })

      const validate = () => {
          formRef.value.validate().then(bln_success =>{
            if(bln_success){
              return true
            }else{
              console.log('One or more fields are not valid')
              return false
            }
          })
      }

      const reset = () => {
        formRef.value.resetValidation()
      }

      const onSubmit = () => {
        const bln_isValid = formRef.value.validate()
        if (bln_isValid) {
          emit('submit', formData)
          reset()
        }
      }

      return {
        formRef: formRef,
        formData: formData,
        validate,
        reset,
        onSubmit
      }
    }
  }
  </script>

  <style scoped>
  .auth-form {
    width: 100%;
    max-width: 400px;
    padding: 20px;
  }
  </style>