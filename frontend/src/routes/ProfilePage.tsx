import { mockUser } from '../utils/mockData';

function ProfilePage() {
    return (
        <div>
            {/* Affichage du nom complet de l'utilisateur */}
            <h1>{mockUser.firstname} {mockUser.lastname}</h1>
        </div>
    );
}

export default ProfilePage;
