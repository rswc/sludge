<template>
    <h1>Transfers</h1>

    <q-card flat bordered class="q-ma-md q-gutter-md">
        <h2>New Transfer</h2>
        <div class="row q-ma-md q-gutter-md">
            <div class="col q-gutter-md">
                <q-select
                    outlined
                    v-model="newTransfer.id_resource"
                    :options="allResources"
                    option-label="name"
                    label="Resource"
                    :error-message="v$.id_resource.$error ? v$.id_resource.$errors[0].$message.toString() : ''"
                    :error="v$.id_resource.$error">
                    <template v-slot:selected-item="scope">
                        {{ scope.opt.name }}
                    </template>
                </q-select>
    
                <q-input
                    outlined
                    v-model.number="newTransfer.amount"
                    label="Amount"
                    type="number"
                    min="0"
                    :error-message="v$.amount.$error ? v$.amount.$errors[0].$message.toString() : ''"
                    :error="v$.amount.$error" />
                    
                <q-select
                    outlined
                    v-model="newTransfer.id_worker"
                    :options="filteredEmployees"
                    :option-label="opt => `${opt.name} ${opt.surname}`"
                    use-input
                    input-debounce="0"
                    label="Employee"
                    @filter="filterFn"
                    :error-message="v$.id_worker.$error ? v$.id_worker.$errors[0].$message.toString() : ''"
                    :error="v$.id_worker.$error">
                    <template v-slot:selected-item="scope">
                        <span>
                            {{ scope.opt.name }} {{ scope.opt.surname }}
                        </span>
                    </template>
                </q-select>
            </div>
                
            <div class="col q-gutter-md">
                <q-select
                    outlined
                    v-model="newTransfer.id_facility_src"
                    :options="allFacilities"
                    option-label="name"
                    label="Source facility"
                    :error-message="v$.id_facility_src.$error ? v$.id_facility_src.$errors[0].$message.toString() : ''"
                    :error="v$.id_facility_src.$error">
                    <template v-slot:selected-item="scope">
                        {{ scope.opt.name }}
                    </template>
                </q-select>

                <q-select
                    outlined
                    v-model="newTransfer.id_facility_dst"
                    :options="allFacilities"
                    option-label="name"
                    label="Destination facility"
                    :error-message="v$.id_facility_dst.$error ? v$.id_facility_dst.$errors[0].$message.toString() : ''"
                    :error="v$.id_facility_dst.$error">
                    <template v-slot:selected-item="scope">
                        {{ scope.opt.name }}
                    </template>
                </q-select>
                
                <q-btn color="primary" @click="addTransfer" label="Add" :loading="updating" :disable="updating">
                    <template v-slot:loading>
                        <q-spinner />
                    </template>
                </q-btn>
            </div>
        </div>
    </q-card>

    <q-btn color="negative" @click="deleteClicked" label="Clear" :disable="updating" />

    <Spinner v-if="fetching" />

    <div class="row">
        <div class="col fw-bold">
            Resource
        </div>
        <div class="col fw-bold">
            Amount
        </div>
        <div class="col fw-bold">
            Employee
        </div>
        <div class="col fw-bold">
            Date
        </div>
        <div class="col fw-bold">
            From
        </div>
        <div class="col fw-bold">
            To
        </div>
    </div>

    <div class="row" v-for="transfer in transfers">
        <TransferRow :transfer="transfer" />
    </div>

    <q-dialog v-model="showDelete">
        <q-card style="min-width: 350px">
            <q-card-section>
                <div class="text-h6">Delete all transfers?</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
                All {{ transfers.length }} {{ (transfers.length != 1) ? 'transfers' : 'transfer' }}
                will be deleted.<br>This action cannot be undone.
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
                <q-btn flat color="dark" label="Cancel" v-close-popup />
                <q-btn
                    flat
                    color="negative"
                    label="Delete"
                    @click="deleteTransfers" 
                    v-close-popup />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script lang="ts" setup>
import TransferRow from '@/components/TransferRow.vue';
import Spinner from '@/components/Spinner.vue';
import type Employee from '@/types/employee';
import type Facility from '@/types/facility';
import type Resource from '@/types/resource';
import type Transfer from '@/types/transfer';
import useVuelidate from '@vuelidate/core';
import { required, minValue } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';


const fetching = ref(true)
const updating = ref(false)
const transfers = ref<Transfer[]>([])
const newTransfer = ref(new class implements Transfer {
    id_transfer = -1
    timestamp = ''
    id_resource = undefined as any
    id_worker = undefined as any
    amount = 0
    id_facility_src = undefined as any
    id_facility_dst = undefined as any
}())

const allResources = ref<Resource[]>([])
const allFacilities = ref<Facility[]>([])
const allEmployees = ref<Employee[]>([])
const filteredEmployees = ref<Employee[]>([])

const showDelete = ref(false)

const rules = {
    id_resource: { required },
    id_worker: { required },
    amount: { required, minValue: minValue(1e-3) },
    id_facility_src: { required },
    id_facility_dst: { required }
}

const v$ = useVuelidate(rules, newTransfer)

const $q = useQuasar()

const api_hostname = import.meta.env.VITE_API_HOSTNAME


const getTransfers = () => {
    fetching.value = true

    fetch(`${api_hostname}transfer`)
        .then(response => response.json())
        .then(response => {
            transfers.value = response
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

const addTransfer = async () => {
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return

    updating.value = true

    if (newTransfer.value.id_facility_dst.hasOwnProperty('id_facility')) {
        newTransfer.value.id_facility_dst = newTransfer.value.id_facility_dst.id_facility
    }
    if (newTransfer.value.id_facility_src.hasOwnProperty('id_facility')) {
        newTransfer.value.id_facility_src = newTransfer.value.id_facility_src.id_facility
    }
    if (newTransfer.value.id_resource.hasOwnProperty('id_resource')) {
        newTransfer.value.id_resource = newTransfer.value.id_resource.id_resource
    }
    if (newTransfer.value.id_worker.hasOwnProperty('id_worker')) {
        newTransfer.value.id_worker = newTransfer.value.id_worker.id_worker
    }

    fetch(`${api_hostname}transfer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newTransfer.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_transfer')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Transfer logged'
                        })

                        getTransfers()
                    }
                })

                newTransfer.value = new class implements Transfer {
                    id_transfer = -1
                    timestamp = ''
                    id_resource = undefined as any
                    id_worker = undefined as any
                    amount = 0
                    id_facility_src = undefined as any
                    id_facility_dst = undefined as any
                }()

                v$.value.$reset()

            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add transfer'
                    })
                })
            }
        })
        .catch(() => {
            updating.value = false

            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
        })
}

const getResources = () => {
    fetch(`${api_hostname}resource`)
        .then(response => response.json())
        .then(response => {
            allResources.value = response

            if (Array.isArray(response) && response.length > 0) {
                newTransfer.value.id_resource = response[0]
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

const getFacilities = () => {
    fetch(`${api_hostname}facility`)
        .then(response => response.json())
        .then(response => {
            allFacilities.value = response
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

const deleteTransfers = () => {
    fetching.value = true

    fetch(`${api_hostname}transfer`, {method: 'DELETE'})
        .then(response => {
            getTransfers()
        })
        .catch(() => {
            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
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

const deleteClicked = () => {
    showDelete.value = true
}

onMounted(() => {
    getTransfers()
    getResources()
    getFacilities()
    getEmployees()
})
</script>
