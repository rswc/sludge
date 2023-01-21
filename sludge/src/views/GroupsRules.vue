<template>
    <h1>Edit access rules</h1>

    <h2>{{ group?.name }}</h2>

    <q-card flat bordered class="q-ma-md q-gutter-md">
        <h2>Add rule</h2>
        <div class="row q-pa-md">
            <div class="col q-gutter-md">
                <q-select
                    outlined
                    v-model="newRule.id_role"
                    :options="allRoles"
                    option-label="name"
                    label="Role"
                    use-chips
                    stack-label>
                    <template v-slot:selected-item="scope">
                        <q-chip
                            dense
                            square
                            :tabindex="scope.tabindex"
                            :style="chipStyle(scope.opt.color)"
                            class="q-ma-none">
                            {{ scope.opt.name }}
                        </q-chip>
                    </template>
                </q-select>

                <q-select
                    outlined
                    v-model="newRule.policy"
                    :options="['A', 'D']"
                    :option-label="policyLabel"
                    label="Type">
                </q-select>

                <q-btn color="primary" @click="addRule" label="Add" :loading="updating" :disable="updating">
                    <template v-slot:loading>
                        <q-spinner />
                    </template>
                </q-btn>
            </div>
        </div>
    </q-card>

    <div class="row">
        <div class="col fw-bold">
            Role
        </div>
        <div class="col fw-bold">
            Policy
        </div>
        <div class="col fw-bold">
            Actions
        </div>
    </div>

    <q-separator spaced="lg" />

    <Spinner v-if="fetching" />

    <template v-for="rule in rules">
        <div class="row">
            <div class="col">
                <q-chip
                    dense
                    square
                    :style="chipStyle(rule.role!.color)"
                    class="q-ma-none">
                        {{ rule.role?.name }}
                </q-chip>
            </div>
            <div class="col">
                {{ policyLabel(rule.policy) }}
            </div>
            <div class="col">
                <q-btn outline color="negative" @click="deleteRule(rule.id_group, rule.id_role)" :disable="updating">Delete</q-btn>
            </div>
        </div>
    </template>
</template>

<script lang="ts" setup>
import type Spinner from '@/components/Spinner.vue';
import type Group from '@/types/group';
import type Role from '@/types/role';
import type Rule from '@/types/rule';
import { colors, useQuasar } from 'quasar';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()

const fetching = ref(true)
const updating = ref(false)

const rules = ref<Rule[]>([])
const allRoles = ref<Role[]>([])
const group = ref<Group>()
const newRule = ref(new class implements Rule {
    id_role = null as any
    id_group = Number(route.params.id)
    policy = 'A' as 'A'
})

const policyLabel = (policy: 'A' | 'D') => {
    return {
        A: 'Allow',
        D: 'Deny'
    }[policy]
}

const chipStyle = (color: string) => {
    return {
        'background-color': color,
        color: colors.luminosity(color) > 0.5 ? '#000' : '#FFF'
    }
}

const $q = useQuasar()

const api_hostname = import.meta.env.VITE_API_HOSTNAME

const getRoles = () => {
    fetch(`${api_hostname}role`)
        .then(response => response.json())
        .then(response => {
            allRoles.value = response
        })
}

const getRules = () => {
    fetching.value = true

    fetch(`${api_hostname}accessrule?group=${route.params.id}`)
        .then(response => response.json())
        .then(response => {
            fetching.value = false
            rules.value = response
        })
        .catch(_ => {
            fetching.value = false

            $q.notify({
                type: 'negative',
                position: 'bottom-right',
                message: 'An error occured. Please try again later'
            })
        })
}

const getGroup = (id: string) => {
    fetch(`${api_hostname}group/${id}`)
        .then(response => response.json())
        .then(response => {
            group.value = response
        })
}

const addRule = () => {
    if (!newRule.value.id_role) return
    if (!newRule.value.policy) return

    updating.value = true

    if (newRule.value.id_role.hasOwnProperty('id_role')) {
        newRule.value.id_role = newRule.value.id_role.id_role
    }

    fetch(`${api_hostname}accessrule`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newRule.value)
    })
        .then(response => {
            updating.value = false

            if (response.ok) {
                response.json().then(response => {
                    if (response.hasOwnProperty('id_group')) {
                        $q.notify({
                            type: 'positive',
                            position: 'bottom-right',
                            message: 'Rule added'
                        })

                        getRules()
                    }
                })
            } else {
                response.json().then(response => {
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: (response.hasOwnProperty('error')) ? response.error : 'Could not add rule'
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
    
    newRule.value.id_role = null
}

const deleteRule = async (group: number, role: number) => { 
    fetch(`${api_hostname}accessrule/${role}/${group}`, {
            method: "DELETE"
        })
            .then(response => {
                updating.value = false

                if (response.ok) {
                    $q.notify({
                        type: 'positive',
                        position: 'bottom-right',
                        message: 'Rule deleted'
                    })
                    
                    getRules()

                } else
                    $q.notify({
                        type: 'negative',
                        position: 'bottom-right',
                        message: 'Could not delete rule'
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


onMounted(() => {
    getRoles()
    getGroup(route.params.id as string)
    getRules()
})
</script>
