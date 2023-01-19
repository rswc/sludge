<template>
    <h1>Structure</h1>

    <q-card flat bordered class="q-ma-md q-gutter-md">
        <h2>Add Facility</h2>
        <div class="row q-gutter-md">
            <q-input
                outlined
                v-model="newFacility.name"
                label="Name"
                :error-message="v$.name.$error ? v$.name.$errors[0].$message.toString() : ''"
                :error="v$.name.$error" />
            
            <q-input
                outlined
                v-model="newFacility.address"
                label="Address"
                :error-message="v$.address.$error ? v$.address.$errors[0].$message.toString() : ''"
                :error="v$.address.$error" />

            <q-btn color="primary" @click="addFacility" label="Add" :loading="updating" :disable="updating">
                <template v-slot:loading>
                    <q-spinner />
                </template>
            </q-btn>

        </div>
    </q-card>

    <Spinner v-if="fetching" />

    <q-list bordered class="rounded-borders">
        <template v-for="facility in facilities">
            <FacilityRow :facility="facility" @changed="getFacilities" @delete="deleteClicked" />
        </template>
    </q-list>

    <q-dialog v-model="showDelete">
        <q-card style="min-width: 350px">
            <q-card-section>
                <div class="text-h6">Delete facility?</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
                All of its rooms, doors and devices
                will also be deleted.<br>This action cannot be undone.
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
                <q-btn flat color="dark" label="Cancel" v-close-popup />
                <q-btn
                    flat
                    color="negative"
                    label="Delete"
                    @click="deleteFacility(deletingFacility!.id_facility)" 
                    v-close-popup />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script lang="ts" setup>
import Spinner from '@/components/Spinner.vue';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';
import FacilityRow from '@/components/FacilityRow.vue';
import type Facility from '@/types/facility';

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const $q = useQuasar()

const newFacility = ref(new class implements Facility {
    id_facility = -1
    name = ''
    address = ''
}())
const facilities = ref<Facility[]>([])
const fetching = ref(true)
const updating = ref(false)

const showDelete = ref(false)
const deletingFacility = ref<Facility|null>(null)

const rules = {
    name: { required },
    address: { required }
}

const v$ = useVuelidate(rules, newFacility)

const getFacilities = () => {
    fetching.value = true

    fetch(`${api_hostname}facility?include=rooms`)
        .then(response => response.json())
        .then(response => {
            facilities.value = response
            fetching.value = false
        })
        .catch(() => {
            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
        })
}

const addFacility = async () => {
    await v$.value.$validate()
    if (!newFacility.value.name) return
    if (!newFacility.value.address) return

    updating.value = true

    fetch(`${api_hostname}facility`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newFacility.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_facility')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Facility added'
                        })

                        getFacilities()
                    }
                })
            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add facility'
                    })
                })
            }
        })
        .catch(() => {
            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
        })
}

const deleteFacility = async (id: number) => {
    fetch(`${api_hostname}facility/${id}`, {
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
                
                getFacilities()

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

const deleteClicked = (facility: Facility) => {
    deletingFacility.value = facility
    showDelete.value = true
}

onMounted(() => {
    getFacilities()
})
</script>