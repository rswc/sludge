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
            <FacilityRow
                :facility="facility"
                @changed="getFacilities"
                @delete="deleteClicked"
                @test-door="testDoorClicked"
                @test-ap="testAPClicked" />
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

    <q-dialog v-model="showTestDoor">
        <q-card style="min-width: 350px">
            <q-card-section>
                <div class="text-h6">Test door access</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
                Door from {{ testingDoor?.src_name }}
                to {{ testingDoor?.dst_name }}

                <q-select
                    outlined
                    v-model="testWorker"
                    :options="filteredEmployees"
                    :option-label="opt => `${opt.name} ${opt.surname}`"
                    use-input
                    @update:model-value="testResult = null"
                    input-debounce="0"
                    label="Employee"
                    @filter="filterFn">
                    <template v-slot:selected-item="scope">
                        <span>
                            {{ scope.opt.name }} {{ scope.opt.surname }}
                        </span>
                    </template>
                </q-select>

                <q-btn color="primary" @click="testDoor" label="Test" :loading="testing" :disable="testing">
                    <template v-slot:loading>
                        <q-spinner />
                    </template>
                </q-btn>

                <q-card flat v-if="testResult === true">
                    <q-icon name="check" /> Access granted
                </q-card>
                <q-card flat v-else-if="testResult === false">
                    <q-icon name="block" /> Access denied
                </q-card>
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
                <q-btn flat color="dark" label="Close" v-close-popup />
            </q-card-actions>
        </q-card>
    </q-dialog>

    <q-dialog v-model="showTestAP">
        <q-card style="min-width: 350px">
            <q-card-section>
                <div class="text-h6">Test door access</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
                Access Point {{ testingAP?.name }}

                <q-select
                    outlined
                    v-model="testWorker"
                    :options="filteredEmployees"
                    :option-label="opt => `${opt.name} ${opt.surname}`"
                    use-input
                    @update:model-value="testResult = null"
                    input-debounce="0"
                    label="Employee"
                    @filter="filterFn">
                    <template v-slot:selected-item="scope">
                        <span>
                            {{ scope.opt.name }} {{ scope.opt.surname }}
                        </span>
                    </template>
                </q-select>

                <q-btn color="primary" @click="testAP" label="Test" :loading="testing" :disable="testing">
                    <template v-slot:loading>
                        <q-spinner />
                    </template>
                </q-btn>

                <q-card flat v-if="testResult === true">
                    <q-icon name="check" /> Access granted
                </q-card>
                <q-card flat v-else-if="testResult === false">
                    <q-icon name="block" /> Access denied
                </q-card>
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
                <q-btn flat color="dark" label="Close" v-close-popup />
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
import type Employee from '@/types/employee';
import type Door from '@/types/door';
import type AccessPoint from '@/types/accesspoint';

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
const testing = ref(false)

const testWorker = ref<Employee|null>()
const showTestDoor = ref(false)
const testingDoor = ref<Door|null>(null)
const showTestAP = ref(false)
const testingAP = ref<AccessPoint|null>(null)
const testResult = ref<boolean|null>(null)

const showDelete = ref(false)
const deletingFacility = ref<Facility|null>(null)

const allEmployees = ref<Employee[]>([])
const filteredEmployees = ref<Employee[]>([])

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

const getEmployees = () => {
    fetch(`${api_hostname}worker`)
        .then(response => response.json())
        .then(response => {
            allEmployees.value = response
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

const testDoor = () => {
    testing.value = true

    fetch(`${api_hostname}test/door`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id_worker: testWorker.value?.id_worker,
            id_door: testingDoor.value?.id_door
        })
    })
        .then(response => response.json())
        .then(response => {
            testResult.value = response.granted
            testing.value = false
        })
        .catch(() => {
            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })

            testing.value = false
        })
}

const testAP = () => {
    testing.value = true

    fetch(`${api_hostname}test/accesspoint`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id_worker: testWorker.value?.id_worker,
            id_ap: testingAP.value?.id_ap
        })
    })
        .then(response => response.json())
        .then(response => {
            testResult.value = response.granted
            testing.value = false
        })
        .catch(() => {
            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })

            testing.value = false
        })
}

const filterFn = (val: string, update: ((_: () => void) => void)) => {
    if (val === '') {
        update(() => {
            filteredEmployees.value = allEmployees.value
        })
        return
    }

    update(() => {
        const lowerVal = val.toLowerCase()
        filteredEmployees.value = allEmployees.value.filter(v => {
            const fullName = ('' + v.name + v.surname).toLowerCase()
            return fullName.indexOf(lowerVal) > -1
        })
    })
}

const deleteClicked = (facility: Facility) => {
    deletingFacility.value = facility
    showDelete.value = true
}

const testDoorClicked = (door: Door) => {
    testResult.value = null
    testingDoor.value = door
    showTestDoor.value = true
}

const testAPClicked = (ap: AccessPoint) => {
    testResult.value = null
    testingAP.value = ap
    showTestAP.value = true
}

onMounted(() => {
    getFacilities()
    getEmployees()
})
</script>