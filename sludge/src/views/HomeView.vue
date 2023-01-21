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
                <h3>Access events</h3>

                <div class="q-ma-md">
                    Granted {{ stats?.times_granted }} times
                    <q-linear-progress stripe color="positive" size="10px" :value="relGranted" />
    
                    Denied {{ stats?.times_denied }} times
                    <q-linear-progress stripe color="negative" size="10px" :value="relDenied" />
                </div>
                
                <i>(Last 24 hours)</i>
            </q-card>

            <q-card flat bordered class="q-pa-md q-ma-md">
                <h3>Latest transfers</h3>

                <div class="row" style="margin-top: 16px;">
                    <div class="col fw-bold">
                        Resource
                    </div>
                    <div class="col fw-bold">
                        Amount
                    </div>
                    <div class="col-6 fw-bold">
                        Timestamp
                    </div>
                </div>

                <q-separator />

                <div class="row" v-for="transfer in transfers">
                    <div class="col">
                        {{ transfer.resource?.name }}
                    </div>
                    <div class="col">
                        {{ transfer.amount }}
                    </div>
                    <div class="col-6">
                        {{ transfer.timestamp }}
                    </div>
                </div>
            </q-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import type Stats from '@/types/stats';
import type Event from '@/types/event'
import { eventLabel } from '@/types/event'
import { onMounted, ref } from 'vue';
import type Transfer from '@/types/transfer';


const stats = ref<Stats|null>()
const events = ref<Event[]>([])
const transfers = ref<Transfer[]>([])
const relGranted = ref(0)
const relDenied = ref(0)

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const getStats = () => {
    fetch(`${api_hostname}stats`)
        .then(response => response.json())
        .then(response => {
            stats.value = response

            let m = Math.max(response.times_granted, response.times_denied)

            relGranted.value = response.times_granted / m
            relDenied.value = response.times_denied / m
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

const getTransfers = () => {
    fetch(`${api_hostname}transfer?limit=10`)
        .then(response => response.json())
        .then((response) => {
            transfers.value = response
        })
        .catch(() => {
            // do something
        })
}

onMounted(() => {
    getStats()
    getEvents()
    getTransfers()
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
