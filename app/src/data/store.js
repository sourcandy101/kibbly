// The only place the screens get data from.
//
// Preview mode: everything is saved in this browser. To link Firebase, replace
// the bodies of these functions and keep their names and return values. They
// are already async so the screens will not need to change.

import {
  SAMPLE_HOME_ID,
  makeSampleDogs,
  makeSampleHome,
  makeSampleMealLogs,
  makeSampleSchedules,
} from "./sample_data.js";

const STORAGE_KEY = "kibbly_preview_v1";
const USER_KEY = "kibbly_preview_user";

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

function localDayKey(date) {
  return `${date.getFullYear()}_${date.getMonth() + 1}_${date.getDate()}`;
}

function makeSampleState(ownerId, now) {
  const dogs = makeSampleDogs();
  const schedules = makeSampleSchedules();
  return {
    home: makeSampleHome(ownerId, now),
    dogs,
    schedules,
    meals: makeSampleMealLogs(dogs, schedules, now),
    meals_day: localDayKey(now),
  };
}

function readState(now = new Date()) {
  let state = null;
  try {
    state = JSON.parse(readItem(STORAGE_KEY));
  } catch {
    state = null;
  }
  if (!state) state = makeSampleState(readUser()?.id ?? null, now);

  // Sample meals are refreshed each day so the home screen never looks abandoned.
  if (state.meals_day !== localDayKey(now)) {
    state.meals = makeSampleMealLogs(state.dogs, state.schedules, now);
    state.meals_day = localDayKey(now);
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

// Account

export async function getCurrentUser() {
  return readUser();
}

// Preview mode checks no password and never stores one.
export async function signIn(email) {
  const user = { id: `user_${email.trim().toLowerCase()}`, email: email.trim() };
  writeItem(USER_KEY, JSON.stringify(user));
  return user;
}

export async function signOut() {
  removeItem(USER_KEY);
}

// Reading

export async function loadHomeData() {
  const { home, dogs, schedules, meals } = readState();
  return {
    home,
    dogs: [...dogs].sort((a, b) => a.call_order - b.call_order),
    schedules,
    meals,
  };
}

// Writing

export async function saveDog(fields, dogId = null) {
  const state = readState();
  if (dogId) {
    const dog = state.dogs.find((entry) => entry.id === dogId);
    if (!dog) throw new Error("This dog no longer exists.");
    Object.assign(dog, fields);
    writeState(state);
    return dog;
  }
  const dog = {
    ...fields,
    id: makeId("dog"),
    home_id: state.home?.id ?? SAMPLE_HOME_ID,
    photo_urls: [],
    video_url: null,
    voice_clip_url: null,
    call_order: state.dogs.length + 1,
  };
  state.dogs.push(dog);
  writeState(state);
  return dog;
}

// Removes the dog with its schedule and meal history, then closes the gap in the calling order.
export async function deleteDog(dogId) {
  const state = readState();
  state.dogs = state.dogs
    .filter((dog) => dog.id !== dogId)
    .sort((a, b) => a.call_order - b.call_order)
    .map((dog, index) => ({ ...dog, call_order: index + 1 }));
  delete state.schedules[dogId];
  state.meals = state.meals.filter((meal) => meal.dog_id !== dogId);
  writeState(state);
}

// The schedule decides the meal count, so the profile's meals_per_day always follows it.
export async function saveSchedule(dogId, meals) {
  const state = readState();
  const dog = state.dogs.find((entry) => entry.id === dogId);
  if (!dog) throw new Error("This dog no longer exists.");
  state.schedules[dogId] = { dog_id: dogId, home_id: dog.home_id, meals };
  dog.meals_per_day = meals.length;
  writeState(state);
}

export async function saveCallOrder(dogIdsInOrder) {
  const state = readState();
  state.dogs.forEach((dog) => {
    const position = dogIdsInOrder.indexOf(dog.id);
    if (position >= 0) dog.call_order = position + 1;
  });
  writeState(state);
}

export async function resetSampleData() {
  writeState(makeSampleState(readUser()?.id ?? null, new Date()));
}
