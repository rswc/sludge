<template>
    <h1>Events</h1>

    <q-card flat bordered class="q-ma-md q-gutter-md">
        <h2>Filter</h2>
        <div class="row q-ma-md q-gutter-md">
            <div class="col-4">
                <q-input
                outlined
                clearable
                v-model.number="filterData.employee"
                label="Employee" />
            </div>
            
            <div class="col-4">
                <q-select
                    outlined
                    v-model="filterData.type"
                    clearable
                    :options="[0, 1, 2]"
                    :option-label="eventLabel"
                    label="Type">
                </q-select>
            </div>
            
            <div class="col">
                <q-btn color="primary" @click="getEvents" label="Filter" :loading="fetching" :disable="fetching">
                    <template v-slot:loading>
                        <q-spinner />
                    </template>
                </q-btn>
            </div>
        </div>
    </q-card>

    <q-timeline>
        <template v-for="event in events">
            <q-timeline-entry
                :title="eventLabel(event.type)"
                :subtitle="event.timestamp">
                
                <q-chip
                    square
                    icon="person"
                    :ripple="false"
                    class="q-ma-xs">
                    {{ event.worker.name }} {{ event.worker.surname }}
                </q-chip>

                <q-chip
                    square
                    icon="meeting_room"
                    v-if="event.door"
                    :ripple="false"
                    class="q-ma-xs">
                    {{ event.door.src_name }} &rarr; {{ event.door.dst_name }}
                </q-chip>

                <q-chip
                    square
                    icon="devices"
                    v-else-if="event.ap"
                    :ripple="false"
                    class="q-ma-xs">
                    {{ event.ap.name }}
                </q-chip>
                
                {{ event.payload }}
            </q-timeline-entry>
        </template>
    </q-timeline>
</template>

<script lang="ts" setup>
import type Event from '@/types/event';
import { eventLabel } from '@/types/event';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';


const fetching = ref(true)
const events = ref<Event[]>([])
const filterData = ref({
    employee: '',
    type: null
})

const $q = useQuasar()

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const filterParams = () => {
    let params = []

    if (filterData.value.employee) {
        params.push(`employee=${filterData.value.employee}`)
    }
    if (filterData.value.type !== null) {
        params.push(`type=${filterData.value.type}`)
    }
    
    if (params.length > 0) {
        return '?' + params.join('&')
    }

    return ''
}

const getEvents = () => {
    fetching.value = true

    fetch(`${api_hostname}event${filterParams()}`)
        .then(response => response.json())
        .then((response) => {
            events.value = response
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

onMounted(() => {
    getEvents()
})
</script>