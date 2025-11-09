import React from 'react';
import { mockUser } from '../mocks/mockData'; 

function ProfilePage() {
    return (
        <div>
        {/* 2. AFFICHE le nom */}
        <h1>Profil de {mockUser.firstname} {mockUser.lastname}</h1>
        </div>
    );
}

export default ProfilePage;