# Schritt 1: Baue die Vue-Anwendung
FROM node:18 AS build-stage

# Setze das Arbeitsverzeichnis für die Vue-Anwendung
WORKDIR /app/client

# Kopiere package.json und package-lock.json
COPY client/package*.json ./

# Installiere die Abhängigkeiten
RUN npm install

# Kopiere den Rest der Vue-App und baue sie
COPY client/ .
RUN npm run build

# Schritt 2: Erstelle die Flask-Anwendung
FROM python:3.10

# Installieren Sie PostGIS und psql
RUN apt-get update && apt-get install -y \
  postgis \
  postgresql-client \
  && rm -rf /var/lib/apt/lists/*

# Installieren Sie die notwendigen Python-Pakete
RUN pip install psycopg2-binary

# Setze das Arbeitsverzeichnis für die Flask-Anwendung
WORKDIR /app

# Kopiere die Anforderungen der Flask-App und installiere sie
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere die Flask-App
COPY . .

# Kopiere die gebauten statischen Dateien der Vue-App nach Flask's statischem Verzeichnis
COPY --from=build-stage /app/client/dist ./static

# Stelle sicher, dass das statische Verzeichnis existiert, falls `dist` leer ist
RUN mkdir -p ./static

# Setze den Befehl zum Starten der Flask-Anwendung
CMD ["python","-u", "app.py"]