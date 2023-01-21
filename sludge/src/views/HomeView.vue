<template>

    <!-- Top object counts display -->
    <div class="row">
        <div class="col counter bg-green-6">
            <div class="counter-value">{{ stats?.num_workers || 0 }}</div>
            <div class="counter-desc">Employees</div>
        </div>
        
        <div class="col counter bg-secondary">
            <div class="counter-value">{{ stats?.num_rooms || 0 }}</div>
            <div class="counter-desc">Rooms</div>
        </div>

        <div class="col counter">
            <div class="counter-value">{{ stats?.num_doors || 0 }}</div>
            <div class="counter-desc">Doors</div>
        </div>

        <div class="col counter bg-accent">
            <div class="counter-value">{{ stats?.num_aps || 0 }}</div>
            <div class="counter-desc">Access Points</div>
        </div>
    </div>

    <div class="row">
        <div class="col">
            <q-card flat bordered class="q-pa-md q-ma-md">
                <h3>Latest events</h3>
                <q-timeline style="margin-top: 16px;">
                    <template v-for="event in events">
                        <q-timeline-entry
                            :title="eventLabel(event.type)"
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
            </q-card>
        </div>
        <div class="col">
            <q-card flat bordered class="q-pa-md q-ma-md">
                <h3>other stuff</h3>
                
            </q-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import type Stats from '@/types/stats';
import type Event from '@/types/event'
import { eventLabel } from '@/types/event'
import { onMounted, ref } from 'vue';


const stats = ref<Stats|null>()
const events = ref<Event[]>([])

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const getStats = () => {
    fetch(`${api_hostname}stats`)
        .then(response => response.json())
        .then(response => {
            stats.value = response
        })
}

const getEvents = () => {
    fetch(`${api_hostname}event?limit=4`)
        .then(response => response.json())
        .then((response) => {
            events.value = response
        })
        .catch(() => {
            // do something
        })
}

onMounted(() => {
    getStats()
    getEvents()
})
</script>

<style>
.counter {
	display: flex;
	justify-content: center;
	padding: 16px;
	margin: 16px;
	flex-direction: column;
	text-align: center;
    background-color: var(--q-primary);
    color: var(--fbc-light-gray);
    border-radius: 8px;
}

.counter-value {
	font-size: 3em;
	font-weight: bold;
}

.counter-desc {
	opacity: .8;
}
</style>
