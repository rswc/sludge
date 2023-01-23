<template>
    <h1 v-if="route.params.id === 'add'">Add Employee</h1>
    <h1 v-else>Edit Employee</h1>

    <form v-if="employee" class="q-gutter-md" style="max-width: 500px" @submit.prevent="formSubmit">
        <q-input
            outlined
            v-model="(employee.name as any)"
            label="Name"
            :error-message="v$.name.$error ? v$.name.$errors[0].$message.toString() : ''"
            :error="v$.name.$error" />
        <q-input
            outlined
            v-model="(employee.surname as any)"
            label="Surname"
            :error-message="v$.surname.$error ? v$.surname.$errors[0].$message.toString() : ''"
            :error="v$.surname.$error" />
        <q-input
            outlined
            v-model="(employee.job_title as any)"
            label="Job Title"
            :error-message="v$.job_title.$error ? v$.job_title.$errors[0].$message.toString() : ''"
            :error="v$.job_title.$error" />
        <q-input
            outlined
            v-model="(employee.date_of_birth as any)"
            mask="date"
            :rules="['date']"
            label="Date of Birth"
            :error-message="v$.date_of_birth.$error ? v$.date_of_birth.$errors[0].$message.toString() : ''"
            :error="v$.date_of_birth.$error">

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
            :error-message="v$.date_of_expiration.$error ? v$.date_of_expiration.$errors[0].$message.toString() : ''"
            :error="v$.date_of_expiration.$error">

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

        <q-select
            outlined
            v-model="employee.roles"
            multiple
            :options="allRoles"
            option-label="name"
            label="Roles"
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
                    class="q-ma-xs">
                    {{ scope.opt.name }}
                </q-chip>
            </template>
        </q-select>

        <RouterLink to="/employees" custom v-slot="{ navigate }">
            <q-btn color="dark" flat @click="(navigate as any)">Back</q-btn>
        </RouterLink>

        <q-btn color="primary" type="submit" label="Save" :loading="updating" :disable="updating">
            <template v-slot:loading>
                <q-spinner />
            </template>
        </q-btn>
    </form>

</template>

<script lang="ts" setup>
import type Employee from '@/types/employee';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useVuelidate } from '@vuelidate/core'
import { required, helpers } from '@vuelidate/validators';
import { useQuasar, colors } from 'quasar';
import type Role from '@/types/role';

const router = useRouter()
const route = useRoute()

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const fetching = ref(true)
const updating = ref(false)
const employee = ref<Employee>(new class implements Employee {
    id_worker = -1
    name = ''
    surname = ''
    date_of_birth = ''
    date_of_expiration = ''
    job_title = ''
}())
const allRoles = ref<Role[]>([])

const $q = useQuasar()

const validDate = (v: string) => !helpers.req(v) || /^-?[\d]+\/[0-1]\d\/[0-3]\d$/.test(v)

const rules = {
    name: { required },
    surname: { required },
    date_of_birth: { required, validDate },
    date_of_expiration: { validDate },
    job_title: { required }
}

const v$ = useVuelidate(rules, employee as any)

const chipStyle = (color: string) => {
    return {
        'background-color': color,
        color: colors.luminosity(color) > 0.5 ? '#000' : '#FFF'
    }
}

const getRoles = () => {
    fetch(api_hostname + 'role')
        .then(response => response.json())
        .then(response => {
            allRoles.value = response
        })
}

const dateFormat = (d: Date) => {
    return `${d.getFullYear()}/${("0"+(d.getMonth()+1)).slice(-2)}/${("0" + d.getDate()).slice(-2)}`
}

const getEmployee = (id: Number | string) => {
    fetching.value = true

    fetch(`${api_hostname}worker/${id}`)
        .then(response => response.json())
        .then(response => {
            employee.value = response

            if (employee.value.date_of_birth) {
                employee.value.date_of_birth = dateFormat(new Date(employee.value.date_of_birth))
            }
            if (employee.value.date_of_expiration) {
                employee.value.date_of_expiration = dateFormat(new Date(employee.value.date_of_expiration))
            }

            fetching.value = false
        })
        .catch(() => {
            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
        })
}

const updateEmployee = async () => { 
    if (employee.value)
    {
        const isFormCorrect = await v$.value.$validate()
        if (!isFormCorrect) return

        updating.value = true

        fetch(`${api_hostname}worker/${employee.value.id_worker}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(employee.value)
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
}

const createEmployee = async () => {
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return

    updating.value = true

    fetch(`${api_hostname}worker`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(employee.value)
    })
        .then(response => response.json())
        .then(response => {
            updating.value = false
            
            if (response.hasOwnProperty('id_worker')) {
                $q.notify({
                    type: 'positive',
                    position: 'bottom-right',
                    message: 'Employee added'
                })
                
                router.push({name: 'employees'})

                getEmployee(response.id_worker)
            }
        })
        .catch(() => {
            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
        })
}

const formSubmit = () => {
    if (route.params.id === 'add') {
        createEmployee()
    } else {
        updateEmployee()
    }
}

onMounted(() => {
    if (route.params.id !== 'add')
        getEmployee(route.params.id as string)
    
    getRoles()
})
</script>