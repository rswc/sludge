import type Group from '@/types/group'

export default interface AccessPoint {
    id_ap: number,
    name: string,
    id_room: number,
    icon: number,
    groups?: Group[]
}