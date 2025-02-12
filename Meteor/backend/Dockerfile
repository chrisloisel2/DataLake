# Utilisation d'une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make python3-dev libffi-dev librdkafka-dev

RUN pip install --upgrade pip
# Installer les dépendances
RUN pip install -r requirements.txt

# Copier tout le contenu du répertoire courant dans le conteneur
COPY . .

# Définir la commande par défaut
CMD ["python", "app.py"]
