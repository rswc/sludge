<template>
    <template v-if="editing">
         <div class="col q-gutter-md">
             <div class="row q-gutter-sm">
                <q-input
                    outlined
                    v-model="group.name"
                    label="Name"
                    :error-message="v$.name.$error ? v$.name.$errors[0].$message.toString() : ''"
                    :error="v$.name.$error" />
     
                <q-input
                    outlined
                    v-model.number="(group.severity as any)"
                    type="number"
                    label="Severity"
                    :error-message="v$.severity.$error ? v$.severity.$errors[0].$message.toString() : ''"
                    :error="v$.severity.$error" />
             </div>
         </div>
         <div class="col">
             <q-btn color="primary" type="submit" label="Save" :loading="updating" :disable="updating" @click="updateGroup">
                 <template v-slot:loading>
                     <q-spinner />
                 </template>
             </q-btn>
         </div>
     </template>
     <template v-else>
        <div class="col">
            {{ group.name }}
        </div>
        <div class="col">
            {{ group.severity }}
        </div>
        <div class="col actions">
            <q-btn outline color="primary" @click="editing = true">Edit</q-btn>
            <q-btn outline color="negative" @click="deleteGroup" :disable="updating">Delete</q-btn>
        </div>
     </template>
 </template>


<script lang="ts" setup>
import type Group from '@/types/group';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { ref } from 'vue';

const $q = useQuasar()

const updating = ref(false)
const editing = ref(false)

const props = defineProps<{
    group: Group
}>()

const emit = defineEmits(['deleted'])

const rules = {
    name: { required },
    severity: { required }
}

const v$ = useVuelidate(rules, props.group)

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const deleteGroup = async () => { 
    if (props.group)
    {
        updating.value = true

        fetch(`${api_hostname}group/${props.group.id_group}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Group deleted'
                    })
                    
                    emit('deleted')

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete group'
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

const updateGroup = async () => {
    if (props.group)
    {
        updating.value = true

        fetch(`${api_hostname}group/${props.group.id_group}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(props.group)
        })
            .then(response => {
                updating.value = false
                editing.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Group updated'
                    })

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not update group'
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
