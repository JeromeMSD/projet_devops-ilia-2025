export type AuthUser = {
    id_user: string
    firstname: string
    lastname: string
    email: string
    role: 'USER' | 'SRE' | 'ADMIN'
    token?: string | null
    created_at: string
}

export type LoginResponse = {
    message: string
    user: AuthUser
}
