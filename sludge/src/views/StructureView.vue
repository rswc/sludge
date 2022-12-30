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
            <FacilityRow :facility="facility" @changed="getFacilities" />
        </template>
    </q-list>
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

const rules = {
    name: { required },
    address: { required }
}

const v$ = useVuelidate(rules, newFacility)

const getFacilities = () => {
    fetching.value = true

    fetch(`${api_hostname}facility`)
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
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return

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

onMounted(() => {
    getFacilities()
})
</script>