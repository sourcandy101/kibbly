# App

Owner web app: dog profiles, meal schedule, calling order, and later notifications and the meal diary. Built with React and Vite as a PWA, so it runs in any phone browser and can be installed.

Owner: Moetaz El Ouaer.

## Status

| Part | State |
|---|---|
| Login, home, dog profiles, schedule, calling order | Working in preview mode |
| Data model | Follows `schemas/`, in flat collections with `home_id`. A test checks saved documents against the schema files |
| Firebase | Not linked: preview mode saves data in the browser and has no real accounts |
| Photos, video, voice, meal diary, notifications, AI screens | Not started |
| Home settings (kibble `kcal_per_kg`, timezone) | Not started. The home uses the device timezone and an empty kibble entry |
| Body condition pictures | Words for now; the schema expects the owner to choose from pictures |

`npm install` needs a network that allows `registry.npmjs.org`. The campus WiFi networks tested so far block it, but a phone hotspot works.

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
| `src/logic/` | Form rules, meal status, time rules and navigation, with no Firebase code |
| `src/data/store.js` | The only file screens get data from. Replace its function bodies to link Firebase |
| `src/data/sample_data.js` | Sample documents for preview mode |
| `src/data/schema_contract.test.js` | Checks saved documents against `schemas/` |

## Notes for the team

1. `meals_per_day` is not stored because the schema does not allow it. The number of meals comes from the schedule.
2. The feeding plan generator in `ai/` still takes `age_months`, `weight_kg` and `meals_per_day` as input. The feeding plan screen is not built yet; the app can compute all three when it is, unless `ai_v2` changes this input first.
