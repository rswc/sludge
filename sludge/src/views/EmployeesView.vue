<template>
    <h1>Employees</h1>
    <q-btn color="primary" @click="getEmployees">Refresh</q-btn>
    <RouterLink to="/employees/add" custom v-slot="{ navigate }">
        <q-btn color="primary" @click="(navigate as any)">New Employee</q-btn>
    </RouterLink>

    <!-- Header -->
    <div class="row">
        <div class="col fw-bold">
            Name
        </div>
        <div class="col fw-bold">
            Surname
        </div>
        <div class="col fw-bold">
            Date of Birth
        </div>
        <div class="col fw-bold">
            Actions
        </div>
    </div>

    <Spinner v-if="fetching" />

    <div class="row" v-for="emp in employees">
        <EmployeeRow :employee="emp" />
    </div>
</template>

<script lang="ts" setup>
import EmployeeRow from '@/components/EmployeeRow.vue';
import Spinner from '@/components/Spinner.vue';
import type Employee from '@/types/employee';
import { ref } from 'vue';

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const employees = ref<Employee[]>([])
const fetching = ref(true)

const getEmployees = () => {
    fetching.value = true

    fetch(api_hostname + 'worker')
        .then(response => response.json())
        .then(response => {
            employees.value = response
            fetching.value = false
        })
}

getEmployees()
</script>

<style>
.fw-bold {
    font-weight: bold;
}
</style>
