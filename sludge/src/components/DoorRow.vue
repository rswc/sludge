<template>
    <q-expansion-item
        expand-separator
        icon="meeting_room"
        default-opened
        :label="`Door #${door.id_door}`"
        caption="From HERE to SOMEWHERE / From SOMEWHERE to HERE">
        <q-card>
            <q-card-actions>
                <q-btn color="negative" flat @click="deleteDoor">Delete</q-btn>
            </q-card-actions>
            <q-card-section>
                <i>Door form</i>
            </q-card-section>
        </q-card>
    </q-expansion-item>
</template>


<script lang="ts" setup>
import type Door from '@/types/door';
import { useQuasar } from 'quasar';
import { ref } from 'vue';

const props = defineProps<{
    door: Door
}>()

const emit = defineEmits(['deleted', 'changed', 'addDoor'])

const $q = useQuasar()

const updating = ref(false)

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
            .catch(() => {
                $q.notify({
                    type: 'negative',
                    position: 'bottom-right',
                    message: 'An error occured. Please try again later'
                })
            })
    }
}
</script>
