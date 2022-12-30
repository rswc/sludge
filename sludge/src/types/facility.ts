import type Room from '@/types/room'

export default interface Facility {
    id_facility: number,
    name: string,
    address: string,
    rooms?: Room[]
}