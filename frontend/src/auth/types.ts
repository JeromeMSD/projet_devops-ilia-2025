export type AuthUser = {
    user_id: string
    username: string
    email: string
    role: 'user' | 'sre' | 'admin'
    created_at: string
}

export type LoginResponse = {
    message: string
    token: string
    user: AuthUser
}
