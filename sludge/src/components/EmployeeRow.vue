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
            <q-btn outline color="primary" @click="(navigate as any)" :disable="updating">Edit</q-btn>
        </RouterLink>
        <q-btn outline color="negative" @click="deleteEmployee" :disable="updating">Delete</q-btn>
    </div>
</template>

<script lang="ts" setup>
import type Employee from '@/types/employee';
import { useQuasar } from 'quasar';
import { computed, ref } from 'vue';

const $q = useQuasar()

const updating = ref(false)

const props = defineProps<{
    employee: Employee
}>()

const emit = defineEmits(['deleted'])

const editPath = computed(() => {
    return '/employees/' + props.employee.id_worker
})

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const deleteEmployee = async () => { 
    if (props.employee)
    {
        updating.value = true

        fetch(`${api_hostname}worker/${props.employee.id_worker}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Employee deleted'
                    })
                    
                    emit('deleted')

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete employee'
                    })
            })
    }
}
</script>

<style scoped>
.actions button {
    margin: 2px 4px;
}
</style>