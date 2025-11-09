import React from 'react';
import { mockUser } from '../mocks/mockData';
function ProfilePage() {
    return (
        <div>
        <h1>Profil de {mockUser.firstname} {mockUser.lastname}</h1>
        <p>{mockUser.email}</p>
        <p>Rôle: {mockUser.role}</p>
        </div>
    );
}
export default ProfilePage;