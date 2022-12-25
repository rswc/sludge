<template>
    <h1>Employee edit</h1>
    {{ $route.params.id }}

    <form v-if="employee">
        <div class="form-floating mb-3">
            <input type="text" class="form-control" id="form_empName" v-model="employee.name">
            <label for="form_empName" class="form-label">Name</label>
        </div>
        <div class="form-floating mb-3">
            <input type="text" class="form-control" id="form_empSurname" v-model="employee.surname">
            <label for="form_empSurname" class="form-label">Surname</label>
        </div>
        <div class="form-floating mb-3">
            <input type="text" class="form-control" id="form_empTitle" v-model="employee.job_title">
            <label for="form_empTitle" class="form-label">Job Title</label>
        </div>
        <div class="form-floating mb-3">
            <input type="date" class="form-control" id="form_empBirth" v-model="employee.date_of_birth">
            <label for="form_empBirth" class="form-label">Date of Birth</label>
        </div>
        <div class="form-floating mb-3">
            <input type="date" class="form-control" id="form_empExpiration" v-model="employee.date_of_expiration">
            <label for="form_empExpiration" class="form-label">Account expires by</label>
        </div>
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

const getEmployee = () => {
    fetching.value = true

    fetch(api_hostname + 'worker/' + route.params.id)
        .then(response => response.json())
        .then(response => {
            employee.value = response
            fetching.value = false
        })
}

getEmployee()
</script>