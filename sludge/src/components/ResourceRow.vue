<template>
    <template v-if="editing">
         <div class="col q-gutter-md">
             <div class="row q-gutter-sm">
                <q-input
                    outlined
                    v-model="resource.name"
                    label="Name"
                    :error-message="v$.name.$error ? v$.name.$errors[0].$message.toString() : ''"
                    :error="v$.name.$error" />

             </div>
         </div>
         <div class="col">
             <q-btn color="primary" type="submit" label="Save" :loading="updating" :disable="updating" @click="updateResource">
                 <template v-slot:loading>
                     <q-spinner />
                 </template>
             </q-btn>
         </div>
     </template>
     <template v-else>
        <div class="col">
            {{ resource.name }}
        </div>
        <div class="col actions">
            <q-btn outline color="primary" @click="editing = true">Edit</q-btn>
            <q-btn outline color="negative" @click="$emit('delete', resource)" :disable="updating">Delete</q-btn>
        </div>
     </template>
 </template>


<script lang="ts" setup>
import type Resource from '@/types/resource';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { ref } from 'vue';

const $q = useQuasar()

const updating = ref(false)
const editing = ref(false)

const props = defineProps<{
    resource: Resource
}>()

const emit = defineEmits(['delete'])

const rules = {
    name: { required }
}

const v$ = useVuelidate(rules, props.resource)

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const updateResource = async () => {
    if (props.resource)
    {
        updating.value = true

        fetch(`${api_hostname}resource/${props.resource.id_resource}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(props.resource)
        })
            .then(response => {
                updating.value = false
                editing.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Resource updated'
                    })

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not update resource'
                    })
            })
            .catch(() => {
                $q.notify({
                    type: 'negative',
                    position: 'bottom-right',
                    message: 'An error occured. Please try again later'
                })
            })
    }
}
</script>
