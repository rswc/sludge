<template>
    <q-expansion-item
        expand-separator
        icon="apartment"
        default-opened
        :label="facility.name"
        :caption="facility.address">
        <q-card>
            <q-card-actions>
                <q-btn color="primary" flat @click="editClicked">Edit</q-btn>
                <q-btn color="primary" flat>Add room</q-btn>
                <q-btn color="negative" flat @click="deleteResource">Delete</q-btn>
            </q-card-actions>
            <q-card-section>
                <i>No rooms</i>
            </q-card-section>
        </q-card>
        <q-dialog v-model="editing">
            <q-card style="min-width: 350px">
                <q-card-section>
                    <div class="text-h6">Edit facility</div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                    <q-input
                        outlined
                        v-model="editedFacitlity.name"
                        bottom-slots
                        :rules="[v => !!v || 'Field is required']"
                        label="Name" />
                    
                    <q-input
                        outlined
                        v-model="editedFacitlity.address"
                        bottom-slots
                        :rules="[v => !!v || 'Field is required']"
                        label="Address" />
                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                    <q-btn flat color="dark" label="Cancel" v-close-popup />
                    <q-btn flat label="Save" @click="updateFacility" />
                </q-card-actions>
            </q-card>
        </q-dialog>
    </q-expansion-item>
</template>


<script lang="ts" setup>
import type Facility from '@/types/facility';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { ref } from 'vue';

const props = defineProps<{
    facility: Facility
}>()

const emit = defineEmits(['changed'])

const $q = useQuasar()

const updating = ref(false)
const editing = ref(false)
const editedFacitlity = ref(new class implements Facility {
    id_facility = -1
    name = ''
    address = ''
}())

const rules = {
    name: { required },
    address: { required }
}

const v$$ = useVuelidate(rules, editedFacitlity)

const editClicked = () => {
    editedFacitlity.value = JSON.parse(JSON.stringify(props.facility))
    editing.value = true
}

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const deleteResource = async () => { 
    if (props.facility)
    {
        updating.value = true

        fetch(`${api_hostname}facility/${props.facility.id_facility}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Facility deleted'
                    })
                    
                    emit('changed')

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete facility'
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

const updateFacility = async () => {
    if (editedFacitlity.value.id_facility >= 0)
    {
        const isFormCorrect = await v$$.value.$validate()
        if (!isFormCorrect) return

        updating.value = true

        fetch(`${api_hostname}facility/${editedFacitlity.value.id_facility}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(editedFacitlity.value)
        })
            .then(response => {
                updating.value = false
                editing.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Facility updated'
                    })

                    emit('changed')

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not update facility'
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
