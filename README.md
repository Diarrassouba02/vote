# 🗳️ Vote Président – 6ème 6 San-Pédro

Application de vote pour l'élection du Président de la Promotion 6ème 6 du Lycée de San-Pédro.

## Structure du projet

```
vote-app/
├── backend/
│   ├── app.py           # Serveur Flask (API)
│   ├── votes.json       # Base de données JSON
│   └── requirements.txt
└── frontend/
    └── index.html       # Interface React (tout-en-un)
```

## 🚀 Lancement

### 1. Backend (Python/Flask)

```bash
cd backend
pip install -r requirements.txt
python app.py
```
→ Serveur lancé sur http://localhost:5000

### 2. Frontend

Ouvrir `frontend/index.html` dans le navigateur (ou utiliser un serveur local).

> **Note** : Pour que le frontend communique avec le backend, les deux doivent tourner en même temps.

## 🔌 API Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/candidates` | Liste des candidats |
| POST | `/api/vote` | Enregistrer un vote |
| GET | `/api/results` | Résultats avec pourcentages |
| POST | `/api/check-phone` | Vérifier si un numéro a déjà voté |

### Exemple de vote (POST /api/vote)
```json
{
  "telephone": "0700000000",
  "candidate_id": 1
}
```

## ✅ Règles de vote

- Un numéro de téléphone = **1 seul vote**
- Validation du format de numéro (8–10 chiffres)
- Les votes sont sauvegardés dans `votes.json`

## 📱 Interface

- Design responsive pour smartphone
- Thème sombre aux couleurs de la Côte d'Ivoire
- Onglet **Voter** + onglet **Résultats** en temps réel
