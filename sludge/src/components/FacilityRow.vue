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
                <q-btn color="negative" flat @click="$emit('delete', facility)">Delete</q-btn>
            </q-card-actions>
            <q-card-section>
                <q-list bordered class="q-mx-md rounded-borders" v-if="facility.rooms?.length">
                    <template v-for="room in facility.rooms">
                        <RoomRow
                            :room="room"
                            @changed="roomChanged"
                            @delete="deleteClicked"
                            @add-door="addDoorClicked"
                            @add-ap="addAPClicked"
                            @internal-changed="internalChanged"
                            @test-door="emit('testDoor', $event)"
                            @test-ap="emit('testAp', $event)"
                            ref="roomRows"/>
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
                        :error-message="v$room.name.$error ? v$room.name.$errors[0].$message.toString() : 'no error'"
                        :error="v$room.name.$error"
                        label="Name" />

                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                    <q-btn flat color="dark" label="Cancel" v-close-popup />
                    <q-btn flat label="Save" @click="addRoom" />
                </q-card-actions>
            </q-card>
        </q-dialog>

        <q-dialog v-model="addingDoor">
            <q-card style="min-width: 350px">
                <q-card-section>
                    <div class="text-h6">Add door</div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                    <div class="row">
                        Facility: {{ facility.name }}
                    </div>

                    <q-select
                        outlined
                        v-model="newDoor.id_room_dst"
                        label="Destination room"
                        :options="availableRooms"
                        option-label="name"
                        emit-value
                        bottom-slots
                        :rules="[v => !!v || 'Field is required']">
                    </q-select>

                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                    <q-btn flat color="dark" label="Cancel" v-close-popup />
                    <q-btn flat label="Save" @click="addDoor" />
                </q-card-actions>
            </q-card>
        </q-dialog>

        <q-dialog v-model="addingAP">
            <q-card style="min-width: 350px">
                <q-card-section>
                    <div class="text-h6">Add access point</div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                    <div class="row">
                        Facility: {{ facility.name }}
                    </div>

                    <q-input
                        outlined
                        v-model="newAP.name"
                        bottom-slots
                        :rules="[v => !!v || 'Field is required']"
                        label="Name" />

                    <q-select
                        outlined
                        v-model="newAP.icon"
                        label="Icon"
                        :options="Icons"
                        emit-value
                        bottom-slots
                        :rules="[v => (v >= 0 && v != null) || 'Field is required']">
                        <template v-slot:selected-item="scope">
                            <q-icon :name="Icons[scope.opt].icon"></q-icon>
                        </template>
                    </q-select>

                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                    <q-btn flat color="dark" label="Cancel" v-close-popup />
                    <q-btn flat label="Save" @click="addAP" />
                </q-card-actions>
            </q-card>
        </q-dialog>

        <q-dialog v-model="showDelete">
            <q-card style="min-width: 350px">
                <q-card-section>
                    <div class="text-h6">Delete room?</div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                    All of its doors and access points
                    will also be deleted.<br>This action cannot be undone.
                </q-card-section>

                <q-card-actions align="right" class="text-primary">
                    <q-btn flat color="dark" label="Cancel" v-close-popup />
                    <q-btn
                        flat
                        color="negative"
                        label="Delete"
                        @click="deleteRoom(deletingRoom!.id_room)" 
                        v-close-popup />
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
import { computed, ref } from 'vue';
import RoomRow from './RoomRow.vue';
import type Door from '@/types/door';
import type AccessPoint from '@/types/accesspoint';
import Icons from '@/components/apicons'

const props = defineProps<{
    facility: Facility
}>()

const emit = defineEmits(['changed', 'delete', 'testDoor', 'testAp'])

const $q = useQuasar()

const roomRows = ref<(typeof RoomRow)[]>()

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

const addingDoor = ref(false)
const newDoor = ref(new class implements Door {
    id_door = -1
    id_room_src = -1
    id_room_dst = -1
}())

const addingAP = ref(false)
const newAP = ref(new class implements AccessPoint {
    id_ap = -1
    name = ''
    id_room = -1
    icon = -1
}())

// As in, available destination rooms (for doors)
// assuming door cannot lead back into its source room
const availableRooms = computed(() => {
    return props.facility.rooms?.filter(v => v.id_room !== newDoor.value.id_room_src)
})

const showDelete = ref(false)
const deletingRoom = ref<Room|null>()

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

const updateFacility = async () => {
    if (editedFacitlity.value.id_facility >= 0)
    {
        const isFormCorrect = await v$editFacility.value.$validate()

        if (!editedFacitlity.value.address) return
        if (!editedFacitlity.value.name) return

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
    // Vuelidate just doesn't work here for some reason
    if (!newRoom.value.name) return

    // const isFormCorrect = await v$room.value.$validate()
    // if (!isFormCorrect) {
    //     console.error('Form incorrect', v$room.value.$errors, v$room.value.name.$model)
    //     return
    // }

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

const addDoor = async () => {
    updating.value = true

    // Quasar select element will not cooperate on correctly displaying
    // option label and passing option value along otherwise
    newDoor.value.id_room_dst = (newDoor.value.id_room_dst as any).id_room

    if (newDoor.value.id_room_dst < 0) return

    fetch(`${api_hostname}door`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newDoor.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_door')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Door added'
                        })

                        for (const room of roomRows.value!) {
                            room.getRoom()
                        }

                        addingDoor.value = false
                    }
                })
            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add door'
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

const addAP = async () => {
    updating.value = true

    if (newAP.value.name.length < 1) return

    fetch(`${api_hostname}accesspoint`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newAP.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_ap')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Access Point added'
                        })

                        for (const room of roomRows.value!) {
                            room.getRoom()
                        }

                        addingAP.value = false
                    }
                })
            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add Access Point'
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

const deleteRoom = async (id: number) => { 
    fetch(`${api_hostname}room/${id}`, {
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

                roomDeleted(id)

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

const addDoorClicked = (id: number) => {
    newDoor.value = new class implements Door {
        id_door = -1
        id_room_src = id
        id_room_dst = undefined as any // yeah, alright
    }()
    addingDoor.value = true
}

const addAPClicked = (id: number) => {
    newAP.value = new class implements AccessPoint {
        id_ap = -1
        name = ''
        id_room = id
        icon = 0
    }()
    addingAP.value = true
}

const deleteClicked = (room: Room) => {
    deletingRoom.value = room
    showDelete.value = true
}

const internalChanged = () => {
    for (const room of roomRows.value!) {
        room.getRoom()
    }
}
</script>
