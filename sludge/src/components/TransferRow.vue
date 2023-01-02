<template>
    <div class="col">
        {{ transfer.resource?.name }}
    </div>
    <div class="col">
        {{ transfer.amount }}
    </div>
    <div class="col">
        {{ transfer.worker?.name }} {{ transfer.worker?.surname }}
    </div>
    <div class="col">
        {{ transfer.timestamp }}
    </div>
    <div class="col">
        {{ transfer.facility_src?.name }}
    </div>
    <div class="col">
        {{ transfer.facility_dst?.name }}
    </div>
</template>

<script lang="ts" setup>
import type Transfer from '@/types/transfer';

const props = defineProps<{
    transfer: Transfer
}>()

</script>
