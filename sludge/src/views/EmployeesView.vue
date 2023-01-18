<template>
    <h1>Employees</h1>
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
            Job Title
        </div>
        <div class="col-4 fw-bold">
            Roles
        </div>
        <div class="col fw-bold">
            Actions
        </div>
    </div>

    <div class="row q-gutter-md">
        <div class="col fw-bold">
            <q-input
                outlined
                v-model="filterDummy.name"
                autocomplete="off"
                clearable
                label="Name" />
        </div>
        <div class="col fw-bold">
            <q-input
                outlined
                v-model="filterDummy.surname"
                autocomplete="off"
                clearable
                label="Surname" />
        </div>
        <div class="col fw-bold">
            <q-input
                outlined
                v-model="filterDummy.job_title"
                autocomplete="off"
                clearable
                label="Job Title" />
        </div>
        <div class="col-4 fw-bold">
            <q-select
                outlined
                clearable
                v-model="filterDummy.roles"
                multiple
                :options="allRoles"
                option-label="name"
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
        <div class="col fw-bold">
            <q-btn color="primary" @click="getEmployees">Filter</q-btn>
        </div>
    </div>

    <Spinner v-if="fetching" />

    <div class="row" v-for="emp in employees">
        <EmployeeRow :employee="emp" :role-options="allRoles" @deleted="getEmployees" />
    </div>
</template>

<script lang="ts" setup>
import EmployeeRow from '@/components/EmployeeRow.vue';
import Spinner from '@/components/Spinner.vue';
import type Employee from '@/types/employee';
import type Role from '@/types/role';
import { useQuasar, colors } from 'quasar';
import { onMounted, ref } from 'vue';

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const $q = useQuasar()

const employees = ref<Employee[]>([])
const allRoles = ref<Role[]>([])
const fetching = ref(true)
const filterDummy = ref(new class implements Employee {
    id_worker = -1
    name = ''
    surname = ''
    date_of_birth = ''
    date_of_expiration = ''
    job_title = ''
    roles: Role[] = []
}())

const chipStyle = (color: string) => {
    return {
        'background-color': color,
        color: colors.luminosity(color) > 0.5 ? '#000' : '#FFF'
    }
}

const filterParams = () => {
    let params = []

    if (filterDummy.value.name) {
        params.push(`name=${filterDummy.value.name}`)
    }
    if (filterDummy.value.surname) {
        params.push(`surname=${filterDummy.value.surname}`)
    }
    if (filterDummy.value.job_title) {
        params.push(`job_title=${filterDummy.value.job_title}`)
    }

    if (filterDummy.value.roles) {
        for (const role of filterDummy.value.roles) {
            params.push(`role=${role.id_role}`)
        }
    }
    
    if (params.length > 0) {
        return '?' + params.join('&')
    }

    return ''
}

const getEmployees = () => {
    fetching.value = true

    fetch(`${api_hostname}worker${filterParams()}`)
        .then(response => response.json())
        .then(response => {
            employees.value = response
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

const getRoles = () => {
    fetch(api_hostname + 'role')
        .then(response => response.json())
        .then(response => {
            allRoles.value = response
        })
}

onMounted(() => {
    getEmployees()
    getRoles()
})
</script>
