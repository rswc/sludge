import type Employee from "./employee";
import type AccessPoint from "./accesspoint";
import type Door from "./door";

export default interface Event {
    id_event: number,
    timestamp: string,
    type: number,
    id_worker: number,
    payload?: string,
    id_ap?: number,
    id_door?: number,
    worker: Employee,
    ap?: AccessPoint,
    door?: Door
}

const eventTypeName = [
    'Access Granted',
    'Access Denied',
    'Error',
]

const eventLabel = (type: number) => {
    return eventTypeName[type]
}

export { eventTypeName, eventLabel }