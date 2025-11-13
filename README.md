# projet_devops-ilia-2025
Polytech Dijon - ILIA - Projet DevOps 2025


## commande d'instalation 
pip install pytest

### Pour tester il faut faire python pour lancer le serveur
bash
flags/app.py  

####pour voir les differents roles présent: 
http://127.0.0.1:5000/admin/flags

##### pour voir si admin par exemple est dans une des "fonctionalité"
http://127.0.0.1:5000/flags?role=admin
    
### exemple de requete pour rajouter un nouveau flag dans les deux presents pour le moment en la metant dans un autre terminal
bash
Invoke-WebRequest -Uri http://127.0.0.1:5000/admin/flags/new-login-page -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"enabled": true, "description": "Nouvelle page de connexion", "roles": ["sre"]}'

test unitaire :
bash
pytest flags/test_app.py
