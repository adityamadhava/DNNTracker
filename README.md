# DNN Revision Tracker

A Django web app to track your Deep Neural Network (DNN) revision progress. Uses Firebase Firestore as the database and is built for deployment on Vercel.

## Stack

- **Django 4.2** (Python)
- **Firebase Firestore** (via `firebase-admin` SDK)
- **Vercel** (serverless)
- **HTML + Tailwind CSS (CDN)** — server-rendered, no React

## Features

- **Dashboard** — Overall DNN revision progress (% complete)
- **Pre-filled topics** — 13 DNN topics with subtopics
- **Per-topic** — Checkbox to mark complete, notes field, difficulty (Easy/Medium/Hard)
- **Progress bars** — Per topic and overall
- **Revision streak** — Days in a row you studied
- **Filters** — All / Completed / Pending / Difficulty

## Setup

### 1. Create virtual environment

```bash
cd dnn-tracker
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install django firebase-admin python-dotenv
# or: pip install -r requirements.txt
```

### 3. Create .env file

```bash
touch .env
```

Open `.env` and add Firebase credentials using **one** of these:

- **Option A (recommended for local):** Path to your service account JSON file (e.g. the one you downloaded from Firebase):

  ```
  FIREBASE_CREDENTIALS_PATH=dnntracker-firebase-adminsdk-fbsvc-bdf1a73e86.json
  ```

- **Option B:** Paste the entire JSON content as a single line:

  ```
  FIREBASE_CREDENTIALS='paste entire JSON content here'
  ```

Get the JSON from [Firebase Console](https://console.firebase.google.com) → Project Settings → Service accounts → **Generate new private key**. Enable **Firestore** in the project if you haven’t already.

### 4. Seed Firestore

On first run, seed the `dnn_topics` collection:

```bash
python manage.py seed_topics
```

### 5. Run locally

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Deployment on Vercel

### 1. Install Vercel CLI (optional)

```bash
npm i -g vercel
```

### 2. Configure environment variables

In **Vercel Dashboard → Project → Settings → Environment Variables**, add:

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Secret key for Django (generate a random string) |
| `FIREBASE_CREDENTIALS` | Full service account JSON as a **single-line string** |
| `ALLOWED_HOSTS` | e.g. `your-app.vercel.app` (or leave default) |

For `FIREBASE_CREDENTIALS`, paste the whole JSON in one line (no newlines). You can minify the downloaded JSON.

### 3. Deploy

```bash
vercel
```

Or connect the repo to Vercel and deploy from Git. All requests are routed to the Django WSGI app via `vercel.json` and `api/wsgi.py`.

### 4. After first deploy

Firestore is empty until you run the seed command. Options:

- Run **once** locally with production env vars (e.g. set `FIREBASE_CREDENTIALS` to the same value) and run `python manage.py seed_topics`, or
- Add a one-off deploy step / script that calls the seed logic (e.g. a Vercel build command that runs the seed if needed), or
- Use a Firebase Cloud Function or a small script run from your machine that uses the same credentials to seed.

## Project structure

```
dnn-tracker/
├── vercel.json
├── requirements.txt
├── .env.example
├── manage.py
├── api/
│   └── wsgi.py          # Vercel serverless entry
├── dnn_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tracker/
    ├── views.py
    ├── urls.py
    ├── firebase.py      # Firebase init + CRUD
    ├── topics_data.py   # DNN topics + subtopics
    ├── context_processors.py
    ├── templates/
    │   ├── base.html
    │   ├── dashboard.html
    │   └── topic_detail.html
    └── management/commands/
        └── seed_topics.py
```

## Firestore

- **Collection:** `dnn_topics`
- **Document fields:** `topic_name`, `subtopics` (array), `completed_subtopics` (array of indices), `notes`, `last_studied`, `difficulty`, `order`
- **Streak:** `revision_streak` collection, document `current` with `last_date`, `streak_days`

## License

MIT.
