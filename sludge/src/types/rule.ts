import type Role from "./role";

export default interface Rule {
    id_role: number,
    id_group: number,
    policy: 'A' | 'D',
    role?: Role
}