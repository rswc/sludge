<template>
   <template v-if="editing">
        <div class="col q-gutter-md">
            <div class="row q-gutter-sm">
                <q-input
                    outlined
                    v-model="(role.name as any)"
                    label="Name"
                    :error-message="v$.name.$error ? v$.name.$errors[0].$message.toString() : ''"
                    :error="v$.name.$error" />
    
                <q-input
                    outlined
                    v-model="role.color"
                    label="Color"
                    :error-message="v$.color.$error ? v$.color.$errors[0].$message.toString() : ''"
                    :error="v$.color.$error">
                    <template v-slot:append>
                        <q-icon name="colorize" class="cursor-pointer">
                            <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                            <q-color v-model="role.color" />
                            </q-popup-proxy>
                        </q-icon>
                    </template>
                </q-input>
            </div>
        </div>
        <div class="col">
            <q-btn color="primary" type="submit" label="Save" :loading="updating" :disable="updating" @click="updateRole">
                <template v-slot:loading>
                    <q-spinner />
                </template>
            </q-btn>
        </div>
    </template>
    <template v-else>
        <div class="col">
            <q-chip square :style="chipStyle" :ripple="false">
                {{ role.name }}
            </q-chip>
        </div>
        <div class="col">
            {{ role.num_workers }}
        </div>
        <div class="col actions">
            <q-btn outline color="primary" @click="editing = true">Edit</q-btn>
            <q-btn outline color="negative" @click="$emit('delete', role)" :disable="updating">Delete</q-btn>
        </div>
    </template>
</template>

<script lang="ts" setup>
import type Role from '@/types/role';
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import { useQuasar, colors } from 'quasar';
import { computed, ref } from 'vue';

const $q = useQuasar()

const updating = ref(false)
const editing = ref(false)

const props = defineProps<{
    role: Role
}>()

const emit = defineEmits(['delete'])

const chipStyle = computed(() => {
    return {
        'background-color': props.role.color,
        color: colors.luminosity(props.role.color) > 0.5 ? '#000' : '#FFF'
    }
})

const rules = {
    name: { required },
    color: { required }
}

const v$ = useVuelidate(rules, props.role)

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const updateRole = async () => {
    await v$.value.$validate()

    if (!props.role.name) return
    if (!props.role.color) return

    if (props.role)
    {
        updating.value = true

        fetch(`${api_hostname}role/${props.role.id_role}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(props.role)
        })
            .then(response => {
                updating.value = false
                
                if (response.ok) {
                    editing.value = false
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Role updated'
                    })
                    
                } else {
                    response.json().then(response => {
                        $q.notify({
                            type: 'negative',
                            position: 'bottom-right',
                            message: (response.hasOwnProperty('error')) ? response.error : 'Could not update role'
                        })
                    })
                }
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
}
</script>
