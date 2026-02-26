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

## Deploy to Vercel

### Step 1: Import project on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in (e.g. with GitHub).
2. Click **Add New…** → **Project**.
3. **Import** your repo: `adityamadhava/DNNTracker` (or connect GitHub if needed and select it).
4. Leave **Framework Preset** as None; **Root Directory** as `.`; **Build Command** and **Output Directory** empty. Vercel will use `vercel.json` and `api/wsgi.py`.
5. Do **not** deploy yet — add environment variables first.

### Step 2: Set environment variables

In the same import screen (or later: **Project → Settings → Environment Variables**), add:

| Name | Value | Notes |
|------|--------|--------|
| `DJANGO_SECRET_KEY` | A long random string | e.g. run `python3 -c "import secrets; print(secrets.token_urlsafe(40))"` |
| `FIREBASE_CREDENTIALS` | Your **entire** Firebase service account JSON as **one line** | Copy the contents of `dnntracker-firebase-adminsdk-*.json`, remove newlines, paste as the value. On Vercel you cannot use a file path. |
| `ALLOWED_HOSTS` | `your-app.vercel.app` | Optional; add your Vercel domain after first deploy (e.g. `dnntracker.vercel.app`) |

For **FIREBASE_CREDENTIALS**: open your `.json` file, minify it (one line, no line breaks), and paste that string into the value field.

### Step 3: Deploy

Click **Deploy**. Vercel will install dependencies from `requirements.txt` and route all traffic to the Django app via `api/wsgi.py`.

### Step 4: Seed Firestore (first time only)

The serverless app cannot run `manage.py` on Vercel. Seed from your machine once:

```bash
# In your project, with the same FIREBASE_CREDENTIALS as on Vercel (e.g. in .env)
source venv/bin/activate
export FIREBASE_CREDENTIALS="$(cat dnntracker-firebase-adminsdk-fbsvc-bdf1a73e86.json | tr -d '\n')"
python manage.py seed_topics
```

Or set `FIREBASE_CREDENTIALS` in `.env` to the same JSON and run `python manage.py seed_topics`.

### Deploy from CLI (alternative)

```bash
npm i -g vercel
cd dnn-tracker
vercel
```

Add the same environment variables in **Vercel Dashboard → Project → Settings → Environment Variables**, then redeploy if needed.

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
