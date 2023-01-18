import type Role from "./role";

export default interface Employee {
    id_worker: number,
    name: string,
    surname: string,
    date_of_birth: string,
    date_of_expiration: string,
    job_title: string,
    roles?: Role[] 
}

export interface EmployeeStats {
    id_worker: number,
    num_events: number,
    num_transfers: number
}
