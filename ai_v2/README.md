# Kibbly AI v2

Owner: Zaineb Sassi (AI and Data Lead).

A rebuild of the Kibbly AI from scratch, on a stronger foundation. The first version in `ai/` stays as it is: it documents the prompt engineering experiments (v1 to v3) and is not developed further.

## Principles

1. Numbers, decisions and safety live in code. Models perceive (images) or write (text); they never decide how much food a dog gets.
2. Every feature has its own test cases and evaluation before it is called done.
3. Every model sits behind a swappable interface.
4. Never give a medical diagnosis, never invent data, recommend a vet when something is unusual.

## Steps

| Step | Topic | Status |
|---|---|---|
| 1 | Review the AI feature ideas and agree the scope (see `scope.md`) | done |
| 2 | Shared data model (see `../schemas/`) | done, waiting for team review |
| 3 | Architecture of the AI server (see `architecture.md`) | done |
| 4 | Dog recognition | next |
| 5 | Nutrition engine and feeding plan | to do |
| 6 | Meal insights (reports, alerts) | to do |
| 7 | Server API for the ESP32-CAM and the app | to do |

This table is updated at the end of each step.

## Setup

Everything lives on the D: drive (C: is full).

```
cd D:\kibbly\ai_v2
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m uvicorn kibbly_ai.api.app:app --port 8000
```

Then open http://localhost:8000/docs to try the endpoints.
