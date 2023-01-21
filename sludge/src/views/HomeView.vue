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
</template>

<script setup lang="ts">
import type Stats from '@/types/stats';
import { onMounted, ref } from 'vue';


const stats = ref<Stats|null>()

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const getStats = () => {
    fetch(`${api_hostname}stats`)
        .then(response => response.json())
        .then(response => {
            stats.value = response
        })
}

onMounted(() => {
    getStats()
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
