<template>
    <q-expansion-item
        expand-separator
        icon="apartment"
        default-opened
        :label="facility.name"
        :caption="facility.address">
        <q-card>
            <q-card-actions>
                <q-btn color="primary" flat @click="editClicked">Edit</q-btn>
                <q-btn color="primary" flat @click="addRoomClicked">Add room</q-btn>
                <q-btn color="negative" flat @click="deleteFacility">Delete</q-btn>
            </q-card-actions>
            <q-card-section>
                <q-list bordered class="q-mx-md rounded-borders" v-if="facility.rooms?.length">
                    <template v-for="room in facility.rooms">
                        <RoomRow :room="room" @changed="roomChanged" @deleted="roomDeleted"/>
                    </template>
                </q-list>
                <i v-else>No rooms</i>
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
                        v-model="editedFacitlity.name"
                        bottom-slots
                        :rules="[v => !!v || 'Field is required']"
                        label="Name" />
                    
                    <q-input
                        outlined
                        v-model="editedFacitlity.address"
                        bottom-slots
                        :rules="[v => !!v || 'Field is required']"
                        label="Address" />
                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                    <q-btn flat color="dark" label="Cancel" v-close-popup />
                    <q-btn flat label="Save" @click="updateFacility" />
                </q-card-actions>
            </q-card>
        </q-dialog>

        <q-dialog v-model="addingRoom">
            <q-card style="min-width: 350px">
                <q-card-section>
                    <div class="text-h6">Add room</div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                    <div class="row">
                        Facility: {{ facility.name }}
                    </div>

                    <q-input
                        outlined
                        v-model="newRoom.name"
                        bottom-slots
                        :rules="[v => !!v || 'Field is required']"
                        label="Name" />

                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                    <q-btn flat color="dark" label="Cancel" v-close-popup />
                    <q-btn flat label="Save" @click="addRoom" />
                </q-card-actions>
            </q-card>
        </q-dialog>
    </q-expansion-item>
</template>


<script lang="ts" setup>
import type Facility from '@/types/facility';
import type Room from '@/types/room';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar } from 'quasar';
import { ref } from 'vue';
import RoomRow from './RoomRow.vue';

const props = defineProps<{
    facility: Facility
}>()

const emit = defineEmits(['changed'])

const $q = useQuasar()

const updating = ref(false)
const editing = ref(false)
const editedFacitlity = ref(new class implements Facility {
    id_facility = -1
    name = ''
    address = ''
}())

const addingRoom = ref(false)
const newRoom = ref(new class implements Room {
    id_room = -1
    name = ''
    id_facility = -1
    coordinate_x = -1
    coordinate_y = -1
}())

const rules = {
    name: { required },
    address: { required }
}

const roomRules = {
    name: { required }
}

const v$editFacility = useVuelidate(rules, editedFacitlity)
const v$room = useVuelidate(roomRules, newRoom)

const editClicked = () => {
    editedFacitlity.value = JSON.parse(JSON.stringify(props.facility))
    editing.value = true
}

const addRoomClicked = () => {
    newRoom.value = new class implements Room {
        id_room = -1
        name = ''
        id_facility = -1
        coordinate_x = -1
        coordinate_y = -1
    }()
    addingRoom.value = true
}

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const deleteFacility = async () => { 
    if (props.facility)
    {
        updating.value = true

        fetch(`${api_hostname}facility/${props.facility.id_facility}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Facility deleted'
                    })
                    
                    emit('changed')

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete facility'
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

const updateFacility = async () => {
    if (editedFacitlity.value.id_facility >= 0)
    {
        const isFormCorrect = await v$editFacility.value.$validate()
        if (!isFormCorrect) return

        updating.value = true

        fetch(`${api_hostname}facility/${editedFacitlity.value.id_facility}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(editedFacitlity.value)
        })
            .then(response => {
                updating.value = false
                editing.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Facility updated'
                    })

                    emit('changed')

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not update facility'
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

const addRoom = async () => {
    const isFormCorrect = await v$room.value.$validate()
    if (!isFormCorrect) return

    updating.value = true

    fetch(`${api_hostname}facility/${props.facility.id_facility}/room`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newRoom.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_room')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Room added'
                        })

                        if (!props.facility.hasOwnProperty('rooms')) {
                            props.facility.rooms = [] 
                        }

                        props.facility.rooms?.push(response)

                        addingRoom.value = false
                    }
                })
            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add room'
                    })
                })
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

const roomChanged = (newVal: Room) => {
    if (!props.facility.rooms)
        return;
    
    const idx = props.facility.rooms.findIndex(v => v.id_room === newVal.id_room)
    props.facility.rooms.splice(idx, 1, newVal)
}

const roomDeleted = (id: number) => {
    if (!props.facility.rooms)
        return;
    
    const idx = props.facility.rooms.findIndex(v => v.id_room === id)
    props.facility.rooms.splice(idx, 1)
}
</script>
