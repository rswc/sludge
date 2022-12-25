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
    <div class="col actions">
        <RouterLink :to="editPath" custom v-slot="{ navigate }">
            <q-btn outline color="primary" @click="(navigate as any)">Edit</q-btn>
        </RouterLink>
        <q-btn outline color="negative">Delete</q-btn>
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

<style scoped>
.actions button {
    margin: 2px 4px;
}
</style>