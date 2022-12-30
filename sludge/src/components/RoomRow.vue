<template>
    <q-expansion-item
        expand-separator
        icon="place"
        default-opened
        @before-show="getRoom"
        :label="room.name">
        <q-card>
            <q-card-actions>
                <q-btn color="primary" flat @click="editClicked">Edit</q-btn>
                <q-btn color="primary" flat @click="emit('addDoor', room.id_room)">Add door</q-btn>
                <q-btn color="primary" flat>Add access point</q-btn>
                <q-btn color="negative" flat @click="deleteRoom">Delete</q-btn>
            </q-card-actions>
            <q-card-section>
                <q-list bordered class="q-mx-md rounded-borders" v-if="doors.length">
                    <template v-for="door in doors">
                        <DoorRow :door="door" @deleted="getRoom" />
                    </template>
                </q-list>
                <i v-else>Nothing to display</i>
            </q-card-section>
        </q-card>

        <q-dialog v-model="editing">
            <q-card style="min-width: 350px">
                <q-card-section>
                    <div class="text-h6">Edit room</div>
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
import type AccessPoint from '@/types/accesspoint';
import type Door from '@/types/door';
import type Room from '@/types/room';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';
import DoorRow from './DoorRow.vue';

const props = defineProps<{
    room: Room
}>()

const emit = defineEmits(['deleted', 'changed', 'addDoor'])

const $q = useQuasar()

const doors = ref<Door[]>([])
const aps = ref<AccessPoint[]>([])

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

const getRoom = () => {
    fetch(`${api_hostname}room/${props.room.id_room}?include=doors`)
        .then(response => response.json())
        .then(response => {
            if (response.hasOwnProperty('doors')) {
                doors.value = response.doors
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
    getRoom()
})
</script>
