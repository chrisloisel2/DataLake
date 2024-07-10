# Utilisation d'une image de base Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de configuration
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier tout le contenu du répertoire courant dans le conteneur
COPY . .

# Définir la commande par défaut
CMD ["python", "app.py"]
