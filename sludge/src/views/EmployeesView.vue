<template>
    <h1>Employees</h1>
    <button class="btn btn-primary" @click="getEmployees">hello</button>

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

    <div class="d-flex justify-content-center" v-if="fetching">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>

    <div class="row" v-for="emp in employees">
        <EmployeeRow :employee="emp" />
    </div>
</template>

<script lang="ts" setup>
import EmployeeRow from '@/components/EmployeeRow.vue';
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

</style>
