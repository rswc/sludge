<template>
    <h1>Events</h1>

    <q-timeline>
        <template v-for="event in events">
            <q-timeline-entry
                :title="eventTypeName[event.type]"
                :subtitle="event.timestamp">
                
                <q-chip
                    square
                    :ripple="false"
                    class="q-ma-xs">
                    {{ event.worker.name }} {{ event.worker.surname }}
                </q-chip>
                
                {{ event.payload }}
            </q-timeline-entry>
        </template>
    </q-timeline>
</template>

<script lang="ts" setup>
import type Event from '@/types/event';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';

const eventTypeName = [
    'Access Granted',
    'Access Denied',
    'Error',
]


const fetching = ref(true)
const events = ref<Event[]>([])

const $q = useQuasar()

const api_hostname = import.meta.env.VITE_API_HOSTNAME


const getEvents = () => {
    fetching.value = true

    fetch(`${api_hostname}event`)
        .then(response => response.json())
        .then((response: any[]) => {
            events.value = response.reverse()
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