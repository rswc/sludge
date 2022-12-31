import type Group from '@/types/group'

export default interface Door {
    id_door: number,
    id_room_src: number,
    id_room_dst: number,
    src_name?: string,
    dst_name?: string,
    groups?: Group[]
}