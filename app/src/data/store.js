// The only place the screens get data from. Documents follow schemas/ exactly,
// in flat collections with home_id.
//
// Preview mode: everything is saved in this browser. To link Firebase, replace
// the bodies of these functions and keep their names and return values. They
// are already async so the screens will not need to change.

import { deviceTimezone, localDateIn, utcStamp } from "../logic/time.js";
import { MAX_DOGS } from "../logic/validation.js";
import {
  SAMPLE_HOME_ID,
  emptyMedia,
  emptyRecognition,
  makeSampleDogs,
  makeSampleHome,
  makeSampleMeals,
  makeSampleSchedules,
  makeSampleWeights,
} from "./sample_data.js";

const STORAGE_KEY = "kibbly_preview_v2";
const USER_KEY = "kibbly_preview_user";
const SAMPLE_OWNER_ID = "user_sample";
const MAX_ID_LENGTH = 64;

// Used when the browser blocks storage, for example in a private window.
const memoryFallback = new Map();

function readItem(key) {
  try {
    const stored = globalThis.localStorage?.getItem(key);
    if (stored !== null && stored !== undefined) return stored;
  } catch {
    // Storage is blocked, so use the memory copy.
  }
  return memoryFallback.get(key) ?? null;
}

function writeItem(key, value) {
  memoryFallback.set(key, value);
  try {
    globalThis.localStorage?.setItem(key, value);
  } catch {
    // Storage is blocked or full. The memory copy lasts until the page closes.
  }
}

function removeItem(key) {
  memoryFallback.delete(key);
  try {
    globalThis.localStorage?.removeItem(key);
  } catch {
    // Nothing else to clean up.
  }
}

function makeSampleState(ownerId, now) {
  const timezone = deviceTimezone();
  const dogs = makeSampleDogs(now);
  const schedules = makeSampleSchedules(now);
  return {
    home: makeSampleHome(ownerId, timezone, now),
    dogs,
    schedules,
    weights: makeSampleWeights(dogs, now),
    meals: makeSampleMeals(dogs, schedules, timezone, now),
    meals_day: localDateIn(now, timezone),
  };
}

function readState(now = new Date()) {
  let state = null;
  try {
    state = JSON.parse(readItem(STORAGE_KEY));
  } catch {
    state = null;
  }
  if (!state) state = makeSampleState(readUser()?.id ?? SAMPLE_OWNER_ID, now);

  // Sample meals are refreshed each day so the home screen never looks abandoned.
  const today = localDateIn(now, state.home.timezone);
  if (state.meals_day !== today) {
    state.meals = makeSampleMeals(state.dogs, state.schedules, state.home.timezone, now);
    state.meals_day = today;
  }
  writeState(state);
  return state;
}

function writeState(state) {
  writeItem(STORAGE_KEY, JSON.stringify(state));
}

function readUser() {
  try {
    return JSON.parse(readItem(USER_KEY));
  } catch {
    return null;
  }
}

function makeId(prefix) {
  return `${prefix}_${Date.now().toString(36)}${Math.random().toString(36).slice(2, 8)}`;
}

// Ids may only contain letters, digits and underscores.
function userIdFromEmail(email) {
  return `user_${email.trim().toLowerCase().replace(/[^a-z0-9]+/g, "_")}`.slice(0, MAX_ID_LENGTH);
}

// The dog's weight is always a copy of its latest weigh in.
function applyLatestWeight(state, dog) {
  const entries = state.weights.filter((entry) => entry.dog_id === dog.dog_id);
  const latest = entries.reduce((best, entry) => {
    const isNewer = `${entry.measured_on}${entry.entered_at}` >= `${best.measured_on}${best.entered_at}`;
    return isNewer ? entry : best;
  });
  dog.current_weight_kg = latest.weight_kg;
  dog.weight_measured_on = latest.measured_on;
}

// Account

export async function getCurrentUser() {
  return readUser();
}

// Preview mode checks no password and never stores one.
export async function signIn(email) {
  const user = { id: userIdFromEmail(email), email: email.trim() };
  writeItem(USER_KEY, JSON.stringify(user));
  const state = readState();
  state.home.owner_id = user.id;
  writeState(state);
  return user;
}

export async function signOut() {
  removeItem(USER_KEY);
}

// Reading

export async function loadHomeData() {
  const { home, dogs, schedules, weights, meals } = readState();
  return {
    home,
    dogs: [...dogs].sort((a, b) => a.call_order - b.call_order),
    schedules,
    weights,
    meals,
  };
}

// Writing

export async function saveDog(fields, dogId = null) {
  const state = readState();
  const now = utcStamp();
  const { current_weight_kg: weightKg, weight_measured_on: measuredOn, ...profile } = fields;

  let dog;
  if (dogId) {
    dog = state.dogs.find((entry) => entry.dog_id === dogId);
    if (!dog) throw new Error("This dog no longer exists.");
    Object.assign(dog, profile, { updated_at: now });
  } else {
    if (state.dogs.length >= MAX_DOGS) throw new Error(`A home can have at most ${MAX_DOGS} dogs.`);
    dog = {
      ...profile,
      dog_id: makeId("dog"),
      home_id: state.home?.home_id ?? SAMPLE_HOME_ID,
      media: emptyMedia(),
      recognition: emptyRecognition(),
      call_order: state.dogs.length + 1,
      created_at: now,
      updated_at: now,
    };
    state.dogs.push(dog);
  }

  // A new or changed weight becomes a weigh in. Saving without changing it adds nothing.
  const alreadyLogged = state.weights.some(
    (entry) => entry.dog_id === dog.dog_id && entry.measured_on === measuredOn && entry.weight_kg === weightKg,
  );
  if (!alreadyLogged) {
    state.weights.push({
      weight_id: makeId("weight"),
      home_id: dog.home_id,
      dog_id: dog.dog_id,
      measured_on: measuredOn,
      weight_kg: weightKg,
      entered_at: now,
    });
  }
  applyLatestWeight(state, dog);

  writeState(state);
  return dog;
}

// Removes the dog with its schedule, weights and meals, then closes the gap in the calling order.
export async function deleteDog(dogId) {
  const state = readState();
  state.dogs = state.dogs
    .filter((dog) => dog.dog_id !== dogId)
    .sort((a, b) => a.call_order - b.call_order)
    .map((dog, index) => ({ ...dog, call_order: index + 1 }));
  delete state.schedules[dogId];
  state.weights = state.weights.filter((entry) => entry.dog_id !== dogId);
  state.meals = state.meals.filter((meal) => meal.dog_id !== dogId);
  writeState(state);
}

export async function saveSchedule(dogId, meals) {
  const state = readState();
  const dog = state.dogs.find((entry) => entry.dog_id === dogId);
  if (!dog) throw new Error("This dog no longer exists.");
  state.schedules[dogId] = {
    dog_id: dogId,
    home_id: dog.home_id,
    meals,
    daily_total_grams: meals.reduce((sum, meal) => sum + meal.grams, 0),
    plan_source: "owner_edited",
    confirmed_at: utcStamp(),
  };
  writeState(state);
}

export async function saveCallOrder(dogIdsInOrder) {
  const state = readState();
  const now = utcStamp();
  state.dogs.forEach((dog) => {
    const position = dogIdsInOrder.indexOf(dog.dog_id);
    if (position >= 0) {
      dog.call_order = position + 1;
      dog.updated_at = now;
    }
  });
  writeState(state);
}

export async function resetSampleData() {
  writeState(makeSampleState(readUser()?.id ?? SAMPLE_OWNER_ID, new Date()));
}
