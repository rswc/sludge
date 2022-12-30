<template>
    <q-expansion-item
        expand-separator
        icon="place"
        default-opened
        :label="room.name">
        <q-card>
            <q-card-actions>
                <q-btn color="primary" flat @click="editClicked">Edit</q-btn>
                <q-btn color="primary" flat>Add door</q-btn>
                <q-btn color="primary" flat>Add access point</q-btn>
                <q-btn color="negative" flat @click="deleteRoom">Delete</q-btn>
            </q-card-actions>
            <q-card-section>
                <i>Nothing to display</i>
            </q-card-section>
        </q-card>

        <q-dialog v-model="editing">
            <q-card style="min-width: 350px">
                <q-card-section>
                    <div class="text-h6">Edit facility</div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                    <q-input
                        outlined
                        v-model="editedRoom.name"
                        bottom-slots
                        :rules="[v => !!v || 'Field is required']"
                        label="Name" />

                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                    <q-btn flat color="dark" label="Cancel" v-close-popup />
                    <q-btn flat label="Save" @click="updateRoom" />
                </q-card-actions>
            </q-card>
        </q-dialog>
    </q-expansion-item>
</template>


<script lang="ts" setup>
import type Room from '@/types/room';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { ref } from 'vue';

const props = defineProps<{
    room: Room
}>()

const emit = defineEmits(['deleted', 'changed'])

const $q = useQuasar()

const updating = ref(false)
const editing = ref(false)
const editedRoom = ref(new class implements Room {
    id_room = -1
    name = ''
    id_facility = -1
    coordinate_x = -1
    coordinate_y = -1
}())

const roomRules = {
    name: { required }
}

const v$room = useVuelidate(roomRules, editedRoom)

const editClicked = () => {
    editedRoom.value = JSON.parse(JSON.stringify(props.room))
    editing.value = true
}

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const deleteRoom = async () => { 
    if (props.room)
    {
        updating.value = true

        fetch(`${api_hostname}room/${props.room.id_room}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Room deleted'
                    })

                    emit('deleted', props.room.id_room)

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete room'
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

const updateRoom = async () => {
    if (editedRoom.value.id_room >= 0)
    {
        const isFormCorrect = await v$room.value.$validate()
        if (!isFormCorrect) return

        updating.value = true

        fetch(`${api_hostname}room/${editedRoom.value.id_room}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(editedRoom.value)
        })
            .then(response => {
                updating.value = false
                editing.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Room updated'
                    })

                    response.json().then((room) => emit('changed', room))

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not update room'
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
