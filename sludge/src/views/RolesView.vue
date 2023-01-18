<template>
    <h1>Roles</h1>

    <form @submit.prevent="addRole">
        <div class="row q-gutter-md">
            <q-input
                outlined
                v-model="(newRole.name as any)"
                label="Name"
                :error-message="v$.name.$error ? v$.name.$errors[0].$message.toString() : ''"
                :error="v$.name.$error" />

            <q-input
                outlined
                v-model="newRole.color"
                label="Color"
                :error-message="v$.color.$error ? v$.color.$errors[0].$message.toString() : ''"
                :error="v$.color.$error">
                <template v-slot:append>
                    <q-icon name="colorize" class="cursor-pointer">
                        <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-color v-model="newRole.color" />
                        </q-popup-proxy>
                    </q-icon>
                </template>
            </q-input>

            <q-btn color="primary" type="submit" label="Add" :loading="updating" :disable="updating">
                <template v-slot:loading>
                    <q-spinner />
                </template>
            </q-btn>
        </div>
    </form>

    <!-- Header -->
    <div class="row">
        <div class="col fw-bold">
            Role
        </div>
        <div class="col fw-bold">
            Employees
        </div>
        <div class="col fw-bold">
            Actions
        </div>
    </div>

    <Spinner v-if="fetching" />

    <div class="row" v-for="role in roles">
        <RoleRow :role="role" @delete="deleteClicked" />
    </div>

    <q-dialog v-model="showDelete">
        <q-card style="min-width: 350px">
            <q-card-section>
                <div class="text-h6">Delete employee?</div>
            </q-card-section>

            <q-card-section class="q-pt-none">
                {{ deletingRole?.num_workers }} {{ (deletingRole?.num_workers != 1) ? 'employees' : 'employee' }}
                will have this role removed.<br>This action cannot be undone.
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
                <q-btn flat color="dark" label="Cancel" v-close-popup />
                <q-btn
                    flat
                    color="negative"
                    label="Delete"
                    @click="deleteRole(deletingRole!.id_role)" 
                    v-close-popup />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script lang="ts" setup>
import RoleRow from '@/components/RoleRow.vue';
import Spinner from '@/components/Spinner.vue';
import type Role from '@/types/role';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const $q = useQuasar()

const newRole = ref(new class implements Role {
    id_role = -1
    name = ''
    color = '#bffbff'
    num_workers = 0
}())
const roles = ref<Role[]>([])
const fetching = ref(true)
const updating = ref(false)

const showDelete = ref(false)
const deletingRole = ref<Role|null>(null)

const rules = {
    name: { required },
    color: { required }
}

const v$ = useVuelidate(rules, newRole)

const getRoles = () => {
    fetching.value = true

    fetch(api_hostname + 'role')
        .then(response => response.json())
        .then(response => {
            roles.value = response
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

const addRole = async () => {
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return

    updating.value = true

    fetch(`${api_hostname}role`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newRole.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_role')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Role added'
                        })

                        getRoles()
                    }
                })
            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add role'
                    })
                })
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

const deleteRole = async (id: number) => { 
    fetch(`${api_hostname}role/${id}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Role deleted'
                    })

                    getRoles()

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete role'
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

const deleteClicked = (role: Role) => {
    deletingRole.value = role
    showDelete.value = true
}

onMounted(() => {
    getRoles()
})
</script>