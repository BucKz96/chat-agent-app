# Chat Agent App

Une application de messagerie simple entre un **utilisateur** et un **agent automatisé** avec persistance des conversations.

---

## Stack Technique

- **Backend** : FastAPI + Uvicorn + SQLite
- **Frontend** : Vue 3 + vue3-beautiful-chat
- **API** : REST (JSON)
- **Validation** : Pydantic v2
- **Tests** : Pytest avec TestClient
- **Conteneurisation** : Docker + Docker Compose

---

## Lancer l'application

### Clonage + exécution en un clic

```bash
git clone https://github.com/BucKz96/chat-agent-app.git
cd chat-agent-app
docker-compose up --build
```

### Accès

| Interface | URL |
|-----------|-----|
| API Swagger (FastAPI) | http://localhost:8000/docs |
| Frontend Vue 3 | http://localhost:8080 |

---

## Tester l'API

```bash
docker exec -it chat-back pytest
```

### Exemple d'utilisation

```json
POST /chat/
{
  "history": [
    { "sender": "user", "content": "Salut" }
  ]
}
```

Réponse :

```json
{
  "sender": "agent",
  "content": "Bonjour ! Ravie de vous revoir. Que puis-je faire pour vous ?"
}
```

---

## API Endpoints

- `POST /chat/` - Envoyer un message et recevoir une réponse contextuelle
- `GET /chat/history` - Récupérer l'historique des messages
- `DELETE /chat/history` - Effacer l'historique
- `GET /ping/` - Health check basique
- `GET /ping/health` - Health check détaillé (inclut DB)

---

## Configuration

### Variables d'environnement (Backend)

Créez un fichier `.env` dans le dossier `back/` :

```env
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
FRONTEND_URL=http://localhost:8080
DATABASE_PATH=./chat.db
AGENT_NAME=Agent
MAX_HISTORY_LENGTH=50
```

### Variables d'environnement (Frontend)

Créez un fichier `.env` dans le dossier `front/chat-ui-vue3/` :

```env
VUE_APP_API_URL=http://localhost:8000
```

---

## Fonctionnalités

- **Réponses contextuelles** : L'agent répond différemment selon le contenu (bonjour, merci, aide, au revoir, questions)
- **Persistance SQLite** : Les messages sont sauvegardés en base de données
- **Validation stricte** : L'historique doit alterner user/agent
- **Logging complet** : Toutes les requêtes et erreurs sont loggées
- **Health checks** : Endpoints pour monitoring Docker
- **Gestion d'erreurs** : Middleware global avec retours appropriés

---

## Architecture

```
chat-agent-app/
├── back/
│   ├── app/
│   │   ├── api/endpoints/     # Routes HTTP
│   │   ├── core/              # Config + Logging
│   │   ├── schemas/           # Modèles Pydantic
│   │   └── services/          # Logique métier + DB
│   ├── tests/                 # Tests pytest
│   ├── Dockerfile
│   └── requirements.txt
├── front/
│   └── chat-ui-vue3/          # Application Vue 3
├── docker-compose.yml
└── README.md
```

---

## Docker

### Points forts de la configuration

- **Backend** : Non-root user, health check, dépendances séparées du code
- **Frontend** : Volume optimisé pour node_modules
- **Volumes** : Montage sélectif pour éviter d'écraser les dépendances
- **Restart** : Politique `unless-stopped` pour haute disponibilité

---

## Version

- **v1.1.0** — API avec persistance SQLite, logging, health checks et réponses contextuelles
