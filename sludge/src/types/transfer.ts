import type Resource from "./resource";
import type Employee from "./employee";
import type Facility from "./facility";

export default interface Transfer {
    id_transfer: number,
    timestamp: string,
    id_resource: number,
    id_worker  : number,
    amount: number,
    id_facility_src: number,
    id_facility_dst: number,
    resource?: Resource,
    worker?: Employee,
    facility_src?: Facility,
    facility_dst?: Facility
}