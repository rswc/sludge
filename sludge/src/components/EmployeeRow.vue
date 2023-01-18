<template>
    <div class="col">
        {{ employee.name }}
    </div>
    <div class="col">
        {{ employee.surname }}
    </div>
    <div class="col">
        {{ employee.job_title }}
    </div>
    <div class="col-4">
        <q-select
            borderless
            v-model="employee.roles"
            multiple
            :options="roleOptions"
            option-label="name"
            @update:model-value="updateRoles"
            use-chips
            stack-label>
            <template v-slot:selected-item="scope">
                <q-chip
                    removable
                    dense
                    square
                    @remove="scope.removeAtIndex(scope.index)"
                    :tabindex="scope.tabindex"
                    :style="chipStyle(scope.opt.color)"
                    class="q-ma-none">
                    {{ scope.opt.name }}
                </q-chip>
            </template>
        </q-select>
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
import type Role from '@/types/role';
import { useQuasar, colors } from 'quasar';
import { computed, ref } from 'vue';

const $q = useQuasar()

const updating = ref(false)

const props = defineProps<{
    employee: Employee
    roleOptions: Role[]
}>()

const emit = defineEmits(['deleted'])

const editPath = computed(() => {
    return '/employees/' + props.employee.id_worker
})

const chipStyle = (color: string) => {
    return {
        'background-color': color,
        color: colors.luminosity(color) > 0.5 ? '#000' : '#FFF'
    }
}

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
            .catch(() => {
                $q.notify({
                    type: 'negative',
                    position: 'bottom-right',
                    message: 'An error occured. Please try again later'
                })
            })
    }
}

const updateRoles = async () => {
    fetch(`${api_hostname}worker/${props.employee.id_worker}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                roles: props.employee.roles
            })
        })
            .then(response => response.json())
            .then(response => {
                updating.value = false

                $q.notify({
                    type: 'positive',
                    position: 'bottom-right',
                    message: 'Saved'
                })
            })
            .catch(() => {
                $q.notify({
                    type: 'negative',
                    position: 'bottom-right',
                    message: 'An error occured. Please try again later'
                })
            })
}
</script>
