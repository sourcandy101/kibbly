# App

Owner web app: dog profiles, meal schedule, calling order, and later notifications and the meal diary. Built with React and Vite as a PWA, so it runs in any phone browser and can be installed.

Owner: Zaineb Sassi since 28 November 2026 (first version by Moetaz El Ouaer).

## Design

The app uses the look of the pitch deck, so the product and the pitch read as one brand.

| Token | Value | Use |
|---|---|---|
| Blush `#FFE7F0`, cream `#FFF9FB` | page and cards | surfaces |
| Plum `#2E1433`, soft plum `#5E3D63` | text | ink |
| Press pink `#CC2D6E` | main buttons, with a `#9E1F53` press shadow | white text passes contrast here (5:1); the deck's bubblegum `#FF5C9A` does not (2.9:1), so bubblegum is for decoration only |
| Mint, butter, rose, lilac tints | badges and chips | done, warning, problem, quiet |
| Fraunces (soft) | headings, numbers, wordmark | bundled with `@fontsource-variable`, so it works without internet |
| Nunito Sans | everything else | bundled the same way |

Each dog is drawn as the deck character in its own color (`src/components/dog_figure.jsx`). The color comes from the dog id, so it is the same on every phone, and two dogs of one home never share a color. The face shows how the day went: happy, eating, or sad after a skipped or failed meal. The app is light only, like the deck.

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
