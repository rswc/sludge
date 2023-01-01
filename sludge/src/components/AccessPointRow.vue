<template>
    <q-expansion-item
        expand-separator
        :icon="Icons[ap.icon].icon"
        @before-show="getActiveGroups"
        :label="ap.name">
        <q-card>
            <q-card-actions>
                <q-btn color="negative" flat @click="deleteAP">Delete</q-btn>
            </q-card-actions>
            <q-card-section>
                <q-input
                    outlined
                    v-model="editedAP.name"
                    bottom-slots
                    :rules="[v => !!v || 'Field is required']"
                    label="Name" />

                <q-select
                    outlined
                    v-model="editedAP.icon"
                    label="Icon"
                    :options="Icons"
                    emit-value
                    bottom-slots
                    :rules="[v => (v >= 0 && v != null) || 'Field is required']">
                    <template v-slot:selected-item="scope">
                        <q-icon :name="Icons[scope.opt]?.icon"></q-icon>
                    </template>
                </q-select>

                <q-select
                    outlined
                    v-model="editedAP.groups"
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

                <q-btn color="primary" @click="updateAP" label="Save" :loading="updating" :disable="updating">
                    <template v-slot:loading>
                        <q-spinner />
                    </template>
                </q-btn>
            </q-card-section>
        </q-card>
    </q-expansion-item>
</template>

<script lang="ts" setup>
import type AccessPoint from '@/types/accesspoint';
import type Group from '@/types/group';
import { useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';
import Icons from '@/components/apicons'

const props = defineProps<{
    ap: AccessPoint,
    roomId: number
}>()

const emit = defineEmits(['deleted', 'changed'])

const $q = useQuasar()

const updating = ref(false)
const allGroups = ref<Group[]>()
const editedAP = ref(new class implements AccessPoint {
    id_ap = -1
    name = ''
    id_room = -1
    icon = 0
    groups = []
}())

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const deleteAP = async () => { 
    if (props.ap)
    {
        updating.value = true

        fetch(`${api_hostname}accesspoint/${props.ap.id_ap}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Access Point deleted'
                    })

                    emit('deleted', props.ap.id_ap)

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete Access Point'
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
    fetch(`${api_hostname}accesspoint/${props.ap.id_ap}?include=groups`)
        .then(response => response.json())
        .then(response => {
            if (response.hasOwnProperty('groups')) {
                editedAP.value = response
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

const updateAP = async () => {
    if (editedAP.value.name.length < 1 || editedAP.value.icon < 0 || editedAP.value.icon == null) return

    updating.value = true

    fetch(`${api_hostname}accesspoint/${props.ap.id_ap}`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(editedAP.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                $q.notify({
                    type: 'positive',
                    position: 'bottom-right',
                    message: 'Access Point updated'
                })

                emit('deleted')

            } else
                $q.notify({
                    type: 'negative',
                    position: 'bottom-right',
                    message: 'Could not update Access Point'
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
