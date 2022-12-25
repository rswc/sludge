<template>
    <div class="col">
        {{ employee.name }}
    </div>
    <div class="col">
        {{ employee.surname }}
    </div>
    <div class="col">
        {{ employee.date_of_birth }}
    </div>
    <div class="col">
        <button class="btn btn-outline-primary mx-1">Edit</button>
        <button class="btn btn-outline-danger mx-1">Delete</button>
    </div>
</template>

<script lang="ts" setup>
import type Employee from '@/types/employee';

const props = defineProps<{
    employee: Employee
}>()

</script>
