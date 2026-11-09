// Form rules for dog profiles and schedules.
// Field names match the AI code so data passes through without conversion.

export const ACTIVITY_LEVELS = ["low", "medium", "high"];
export const SEX_OPTIONS = ["female", "male"];
export const MAX_MEALS_PER_DAY = 4;
export const GRAM_STEP = 5;
export const MAX_GRAMS_PER_MEAL = 1000; // prototype tank holds 1 kg

const LIMITS = {
  name: 40,
  breed: 60,
  notes: 500,
  age_months: { min: 1, max: 300 },
  weight_kg: { min: 0.5, max: 120 },
};

const TIME_PATTERN = /^([01]\d|2[0-3]):[0-5]\d$/;
const NUMBER_PATTERN = /^\d+(\.\d+)?$/;

// Returns a number, or null when the text is not a plain positive number.
// Accepts a comma as the decimal mark, as many phones type it.
export function parseNumber(raw) {
  const text = String(raw ?? "").trim().replace(",", ".");
  return NUMBER_PATTERN.test(text) ? Number(text) : null;
}

export function validateDog(form) {
  const errors = {};

  const name = String(form.name ?? "").trim();
  if (!name) errors.name = "Enter the dog's name.";
  else if (name.length > LIMITS.name) errors.name = `Use at most ${LIMITS.name} characters.`;

  const breed = String(form.breed ?? "").trim();
  if (!breed) errors.breed = "Enter the breed, or Mixed.";
  else if (breed.length > LIMITS.breed) errors.breed = `Use at most ${LIMITS.breed} characters.`;

  if (!SEX_OPTIONS.includes(form.sex)) errors.sex = "Choose female or male.";

  const age = parseNumber(form.age_months);
  const { min: ageMin, max: ageMax } = LIMITS.age_months;
  if (age === null || !Number.isInteger(age) || age < ageMin || age > ageMax) {
    errors.age_months = `Enter a whole number of months from ${ageMin} to ${ageMax}.`;
  }

  const weight = parseNumber(form.weight_kg);
  const { min: weightMin, max: weightMax } = LIMITS.weight_kg;
  if (weight === null || weight < weightMin || weight > weightMax) {
    errors.weight_kg = `Enter a weight from ${weightMin} to ${weightMax} kg.`;
  }

  if (!ACTIVITY_LEVELS.includes(form.activity)) errors.activity = "Choose low, medium or high.";

  const mealsPerDay = parseNumber(form.meals_per_day);
  if (!Number.isInteger(mealsPerDay) || mealsPerDay < 1 || mealsPerDay > MAX_MEALS_PER_DAY) {
    errors.meals_per_day = `Choose from 1 to ${MAX_MEALS_PER_DAY} meals.`;
  }

  const notes = String(form.notes ?? "").trim();
  if (notes.length > LIMITS.notes) errors.notes = `Use at most ${LIMITS.notes} characters.`;

  const ok = Object.keys(errors).length === 0;
  return {
    ok,
    errors,
    value: ok
      ? {
          name,
          breed,
          sex: form.sex,
          age_months: age,
          weight_kg: weight,
          activity: form.activity,
          meals_per_day: mealsPerDay,
          notes,
        }
      : null,
  };
}

// Returns one error object per row, in the order the rows were given,
// and the clean meals sorted by time when everything is valid.
export function validateSchedule(rows) {
  const rowErrors = rows.map(() => ({}));
  let formError = "";

  if (rows.length < 1) formError = "Add at least one meal.";
  if (rows.length > MAX_MEALS_PER_DAY) formError = `A dog can have at most ${MAX_MEALS_PER_DAY} meals a day.`;

  const seenTimes = new Set();
  const meals = rows.map((row, index) => {
    const time = String(row.time ?? "").trim();
    if (!TIME_PATTERN.test(time)) rowErrors[index].time = "Choose a time.";
    else if (seenTimes.has(time)) rowErrors[index].time = "Another meal already uses this time.";
    seenTimes.add(time);

    const grams = parseNumber(row.grams);
    if (grams === null || grams < GRAM_STEP || grams > MAX_GRAMS_PER_MEAL) {
      rowErrors[index].grams = `Enter ${GRAM_STEP} to ${MAX_GRAMS_PER_MEAL} g.`;
    } else if (grams % GRAM_STEP !== 0) {
      rowErrors[index].grams = `Use a multiple of ${GRAM_STEP} g.`;
    }
    return { time, grams };
  });

  const ok = !formError && rowErrors.every((errors) => Object.keys(errors).length === 0);
  return {
    ok,
    formError,
    rowErrors,
    value: ok ? [...meals].sort((a, b) => a.time.localeCompare(b.time)) : null,
  };
}

const DEFAULT_TIMES = {
  1: ["18:00"],
  2: ["07:30", "18:00"],
  3: ["07:30", "12:30", "18:00"],
  4: ["07:30", "12:00", "15:30", "18:30"],
};

// Suggested meal times for a new schedule. The owner enters the grams.
export function defaultTimes(mealsPerDay) {
  return DEFAULT_TIMES[mealsPerDay] ?? DEFAULT_TIMES[2];
}

// A free time for a new row, preferring the usual meal times.
export function nextFreeTime(usedTimes) {
  const candidates = [...DEFAULT_TIMES[4], ...DEFAULT_TIMES[3], ...DEFAULT_TIMES[1]];
  return candidates.find((time) => !usedTimes.includes(time)) ?? "";
}
