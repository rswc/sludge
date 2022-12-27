<template>
    <h1>Resources</h1>

    <form @submit.prevent="addResource">
        <div class="row q-gutter-md">
            <q-input
                outlined
                v-model="newResource.name"
                label="Name"
                :error-message="v$.name.$error ? v$.name.$errors[0].$message.toString() : ''"
                :error="v$.name.$error" />

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
            Resource
        </div>
        <div class="col fw-bold">
            Actions
        </div>
    </div>

    <Spinner v-if="fetching" />

    <div class="row" v-for="resource in resources">
        <ResourceRow :resource="resource" @deleted="getResources" />
    </div>
</template>

<script lang="ts" setup>
import Spinner from '@/components/Spinner.vue';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';
import type Resource from '@/types/resource';
import ResourceRow from '@/components/ResourceRow.vue';

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const $q = useQuasar()

const newResource = ref(new class implements Resource {
    id_resource = -1
    name = ''
}())
const resources = ref<Resource[]>([])
const fetching = ref(true)
const updating = ref(false)

const rules = {
    name: { required }
}

const v$ = useVuelidate(rules, newResource)

const getResources = () => {
    fetching.value = true

    fetch(`${api_hostname}resource`)
        .then(response => response.json())
        .then(response => {
            resources.value = response
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

const addResource = async () => {
    const isFormCorrect = await v$.value.$validate()
    if (!isFormCorrect) return

    updating.value = true

    fetch(`${api_hostname}resource`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newResource.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_resource')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Resource added'
                        })

                        getResources()
                    }
                })
            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add resource'
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
    getResources()
})
</script>