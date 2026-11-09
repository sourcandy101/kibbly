# App

Owner app: dog profiles, meal schedule, calling order, and later notifications and the meal diary. Built as a web app (PWA) with React and Vite.

Owner: Moetaz El Ouaer.

## Status

| Part | State |
|---|---|
| Login, home, dog profiles, schedule, calling order | Written, not yet run in a browser |
| Form rules and data layer | Tested with a temporary runner, not yet with Vitest |
| `package.json` versions | Not yet installed, no lock file yet |
| Firebase | Not linked: preview mode saves data in the browser and has no real accounts |
| Photos, video, voice, meal diary, notifications, AI screens | Not started |

`npm install` needs a network that allows `registry.npmjs.org`. The campus WiFi networks tested so far block it.

## Run

```
cd app
npm install
npm run dev
npm test
```

## Layout

| Path | Content |
|---|---|
| `src/screens/` | One file per screen |
| `src/components/` | Shared interface pieces |
| `src/logic/` | Form rules, meal status and navigation, with no Firebase code |
| `src/data/store.js` | The only file screens get data from. Replace its function bodies to link Firebase |
| `src/data/sample_data.js` | Sample dogs and meals for preview mode |

## Data

Field names use snake_case and match the AI code. Compared with the handover data model, these were added:

| Field | Where | Why |
|---|---|---|
| `sex` | dogs | Decided in `ai_v2/scope.md` |
| `meals_per_day` | dogs | Required input of the feeding plan generator |
| `home_id` | schedules, meals | Needed for queries and security rules per home |
| `scheduled_time` | meals | Links a meal log to its planned meal |
| `tank_level_percent` | homes | Shown on the home screen |

To confirm with Zaineb and Youssef when the shared data model is agreed.
