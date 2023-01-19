<template>
    <q-expansion-item
        expand-separator
        icon="meeting_room"
        @before-show="getActiveGroups"
        :label="`Door #${door.id_door}`"
        :caption="doorCaption">
        <q-card>
            <q-card-actions>
                <q-btn color="primary" flat @click="$emit('test', door)">Test access</q-btn>
                <q-btn color="negative" flat @click="deleteDoor">Delete</q-btn>
            </q-card-actions>
            <q-card-section>
                <q-select
                    outlined
                    v-model="groups"
                    multiple
                    :options="allGroups"
                    option-label="name"
                    label="Groups"
                    use-chips
                    stack-label>
                    <template v-slot:selected-item="scope">
                        <q-chip
                            removable
                            dense
                            square
                            @remove="scope.removeAtIndex(scope.index)"
                            :tabindex="scope.tabindex"
                            class="q-ma-xs">
                            {{ scope.opt.name }}
                        </q-chip>
                    </template>
                </q-select>

                <q-btn color="primary" @click="updateGroups" label="Save" :loading="updating" :disable="updating">
                    <template v-slot:loading>
                        <q-spinner />
                    </template>
                </q-btn>
            </q-card-section>
        </q-card>
    </q-expansion-item>
</template>

<script lang="ts" setup>
import type Door from '@/types/door';
import type Group from '@/types/group';
import { useQuasar } from 'quasar';
import { computed, onMounted, ref } from 'vue';

const props = defineProps<{
    door: Door,
    roomId: number
}>()

const emit = defineEmits(['deleted', 'test'])

const $q = useQuasar()

const updating = ref(false)
const groups = ref<Group[]>()
const allGroups = ref<Group[]>()

const doorCaption = computed(() => {
    if (props.door.id_room_src === props.roomId) {
        return `To ${props.door.dst_name}`
    }

    return `From ${props.door.src_name}`
})

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const deleteDoor = async () => { 
    if (props.door)
    {
        updating.value = true

        fetch(`${api_hostname}door/${props.door.id_door}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Door deleted'
                    })

                    emit('deleted', props.door.id_door)

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete door'
                    })
            })
            // .catch(() => {
            //     $q.notify({
            //         type: 'negative',
            //         position: 'bottom-right',
            //         message: 'An error occured. Please try again later'
            //     })
            // })
    }
}

const getGroups = () => {
    fetch(`${api_hostname}group`)
        .then(response => response.json())
        .then(response => {
            allGroups.value = response
        })
        .catch(() => {
            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
        })
}

const getActiveGroups = () => {
    fetch(`${api_hostname}door/${props.door.id_door}?include=groups`)
        .then(response => response.json())
        .then(response => {
            if (response.hasOwnProperty('groups')) {
                groups.value = response.groups
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

const updateGroups = async () => {
    updating.value = true

    fetch(`${api_hostname}door/${props.door.id_door}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            groups: groups.value
        })
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                $q.notify({
                    type: 'positive',
                    position: 'bottom-right',
                    message: 'Groups updated'
                })

            } else
                $q.notify({
                    type: 'negative',
                    position: 'bottom-right',
                    message: 'Could not update groups'
                })
        })
        .catch(() => {
            updating.value = false

            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
        })
}

onMounted(() => {
    getGroups()
    getActiveGroups()
})
</script>
