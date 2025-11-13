# projet_devops-ilia-2025
Polytech Dijon - ILIA - Projet DevOps 2025

> [!note]
    Pour tester il faut faire python
    flags/app.py  # pour lancer le serveur 

    pour voir les differents roles présent: 
    http://127.0.0.1:5000/admin/flags

    pour voir si admin par exemple est dans une des "fonctionalité"
    http://127.0.0.1:5000/flags?role=admin
    
    exemple de requete pour rajouter un nouveau flag dans les deux presents pour le moment en la metant dans un autre terminal
    Invoke-WebRequest -Uri http://127.0.0.1:5000/admin/flags/new-login-page -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"enabled": true, "description": "Nouvelle page de connexion", "roles": ["sre"]}'


> [!important]
> Have fun ! 🚀
