<template>
    <h1>Employees</h1>
    <button class="btn btn-primary">hello</button>

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

    <div class="row" v-for="emp in employees">
        <EmployeeRow :employee="emp" />
    </div>
</template>

<script lang="ts" setup>
import EmployeeRow from '@/components/EmployeeRow.vue';
import { ref } from 'vue';


const employees = ref([
    {
        id: 0,
        name: "Rob",
        surname: "Banks",
        date_of_birth: new Date(),
        job_title: "Security Expert"
    },
    {
        id: 0,
        name: "Michael",
        surname: "Jordan",
        date_of_birth: new Date(),
        job_title: "Baller"
    }
]);

</script>

<style>

</style>
