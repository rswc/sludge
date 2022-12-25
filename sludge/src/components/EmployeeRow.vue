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
        <RouterLink class="btn btn-outline-primary mx-1" :to="editPath">Edit</RouterLink>
        <button class="btn btn-outline-danger mx-1">Delete</button>
    </div>
</template>

<script lang="ts" setup>
import type Employee from '@/types/employee';
import { computed } from 'vue';

const props = defineProps<{
    employee: Employee
}>()

const editPath = computed(() => {
    return '/employees/' + props.employee.id_worker
})

</script>
