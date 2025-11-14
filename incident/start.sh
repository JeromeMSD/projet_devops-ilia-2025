#!/bin/bash
redis-server --daemonize yes
# Attendre que Redis réponde
echo "Attente que Redis démarre..."

for i in {1..30}; do
    redis-cli ping &>/dev/null && break
    sleep 0.2
done

# Vérifier si Redis a répondu
if ! redis-cli ping &>/dev/null; then
    echo "Redis n'a pas démarré."
    exit 1
fi

echo "Redis est prêt."


python src/main.py
