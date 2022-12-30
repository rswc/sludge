import type Door from '@/types/door'
import type AccessPoint from '@/types/accesspoint'

export default interface Room {
    id_room: number,
    name: string,
    id_facility?: number,
    coordinate_x: number,
    coordinate_y: number,
    doors?: Door[],
    accessPoints?: AccessPoint[]
}