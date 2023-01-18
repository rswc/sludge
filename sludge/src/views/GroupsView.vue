<template>
    <h1>Groups</h1>

    <form @submit.prevent="addGroup">
        <div class="row q-gutter-md">
            <q-input
                outlined
                v-model="newGroup.name"
                label="Name"
                :error-message="v$.name.$error ? v$.name.$errors[0].$message.toString() : ''"
                :error="v$.name.$error" />

            <q-input
                outlined
                type="number"
                v-model.number="newGroup.severity"
                label="Severity"
                :error-message="v$.severity.$error ? v$.severity.$errors[0].$message.toString() : ''"
                :error="v$.severity.$error">
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
            Group
        </div>
        <div class="col fw-bold">
            Severity
        </div>
        <div class="col fw-bold">
            Doors
        </div>
        <div class="col fw-bold">
            Access Points
        </div>
        <div class="col fw-bold">
            Actions
        </div>
    </div>

    <Spinner v-if="fetching" />

    <div class="row" v-for="group in groups">
        <GroupRow :group="group" @deleted="getGroups" />
    </div>
</template>

<script lang="ts" setup>
import type Group from '@/types/group'
import Spinner from '@/components/Spinner.vue';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';
import GroupRow from '@/components/GroupRow.vue';

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const $q = useQuasar()

const newGroup = ref(new class implements Group {
    id_group = -1
    name = ''
    severity = 0
}())
const groups = ref<Group[]>([])
const fetching = ref(true)
const updating = ref(false)

const rules = {
    name: { required },
    severity: { required }
}

const v$ = useVuelidate(rules, newGroup)

const getGroups = () => {
    fetching.value = true

    fetch(`${api_hostname}group`)
        .then(response => response.json())
        .then(response => {
            groups.value = response
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

const addGroup = async () => {
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return

    updating.value = true

    fetch(`${api_hostname}group`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newGroup.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_group')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Group added'
                        })

                        getGroups()
                    }
                })
            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add group'
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

onMounted(() => {
    getGroups()
})
</script>