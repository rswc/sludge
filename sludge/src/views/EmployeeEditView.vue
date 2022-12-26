<template>
    <h1>Employee edit</h1>

    <form v-if="employee" class="q-gutter-md" style="max-width: 500px" @submit.prevent="updateEmployee">
        <q-input outlined v-model="(employee.name as any)" label="Name" />
        <q-input outlined v-model="(employee.surname as any)" label="Surname" />
        <q-input outlined v-model="(employee.job_title as any)" label="Job Title" />
        <q-input outlined v-model="(employee.date_of_birth as any)" mask="date" :rules="['date']" label="Date of Birth">
            <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date v-model="(employee.date_of_birth as any)">
                    <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                    </q-date>
                </q-popup-proxy>
                </q-icon>
            </template>
        </q-input>
        <q-input
            outlined
            v-model="(employee.date_of_expiration as any)"
            mask="date"
            :rules="[v => /^-?[\d]+\/[0-1]\d\/[0-3]\d$/.test(v) || v.length === 0 || 'Must be a valid date']"
            label="Account expires by"
        >
            <template v-slot:append>
                <q-icon name="event" class="cursor-pointer">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                    <q-date v-model="(employee.date_of_expiration as any)">
                    <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                    </q-date>
                </q-popup-proxy>
                </q-icon>
            </template>
        </q-input>

        <q-btn color="primary" type="submit" label="Save" :loading="updating" :disable="updating">
            <template v-slot:loading>
                <q-spinner />
            </template>
        </q-btn>
    </form>

</template>

<script lang="ts" setup>
import type Employee from '@/types/employee';
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const fetching = ref(true)
const employee = ref<Employee|null>(null)
const updating = ref(false)

const getEmployee = () => {
    fetching.value = true

    fetch(api_hostname + 'worker/' + route.params.id)
        .then(response => response.json())
        .then(response => {
            employee.value = response
            fetching.value = false
        })
}

const updateEmployee = () => {
    
    if (employee.value)
    {
        updating.value = true

        fetch(`http://localhost:8000/api/worker/${employee.value.id_worker}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(employee.value)
        })
            .then(response => response.json())
            .then(response => {
                updating.value = false

                console.log(response);
                
            })
    }
}

getEmployee()
</script>