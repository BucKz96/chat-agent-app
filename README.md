# 💬 Chat Agent App

Une application de messagerie simple entre un **utilisateur** et un **agent automatisé**, développée pour un test technique de recrutement en Python 

---

## 🧠 Stack Technique

- **Backend** : [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn
- **Frontend** : Vue 3 + [vue3-beautiful-chat](https://github.com/mattmezza/vue-beautiful-chat)
- **API** : REST (JSON)
- **Validation** : Pydantic
- **Tests** : Pytest, TestClient, Autocannon
- **Conteneurisation** : Docker, Docker Compose

---

## 🚀 Lancer l'application

### 📦 Clonage + exécution en un clic

```bash
git clone https://github.com/BucKz96/chat-agent-app.git
cd chat-agent-app
docker-compose up --build
```

### 🌐 Accès

| Interface | URL |
|----------|-----|
| 🎯 API Swagger (FastAPI) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 💬 Frontend Vue 3        | [http://localhost:8080](http://localhost:8080) |

---

## 🧪 Tester l'API

```
docker exec -it chat-back pytest    
```

---
```json
POST /chat/
{
  "history": [
    { "sender": "user", "content": "Salut" }
  ]
}
```

✅ Réponse attendue :

```json
{
  "sender": "agent",
  "content": "Ceci est une réponse automatique."
}
```


---

## 🐳 Docker & Volumes

Le projet utilise :

- `NODE_ENV=development` pour que les `devDependencies` soient bien installées
- Un volume **séparé** pour `/app/node_modules` pour éviter les conflits avec le code monté localement
- `CMD ["npm", "run", "serve"]` pour lancer proprement Vue

---

## 🌿 Version

- **v1.1.0** — Frontend Vue 3 dockerisé avec succès, ready for production & test clone 🔥

---

## ✨ Auteur

- Réalisé par **@BucKz96** pour un test Python  

---

## 💬 Bonus

> Ce projet a été conçu pour fonctionner **immédiatement après un `git clone`**, sans aucune config manuelle.
