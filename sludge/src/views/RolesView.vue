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
            Actions
        </div>
    </div>

    <Spinner v-if="fetching" />

    <div class="row" v-for="role in roles">
        <RoleRow :role="role" @deleted="getRoles" />
    </div>
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
}())
const roles = ref<Role[]>([])
const fetching = ref(true)
const updating = ref(false)

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
}

onMounted(() => {
    getRoles()
})
</script>