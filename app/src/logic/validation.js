// Form rules for dog profiles and schedules.
// Output objects use the field names in schemas/, the team's data contract.

export const ACTIVITY_LEVELS = ["low", "medium", "high"];
export const BODY_CONDITIONS = ["thin", "ideal", "overweight"];
export const SEX_OPTIONS = ["female", "male"];
export const MAX_DOGS = 8; // call_order allows up to 8 in schemas/dog.json
export const MAX_MEALS_PER_DAY = 4;
export const GRAM_STEP = 5;
export const MAX_GRAMS_PER_MEAL = 1000; // prototype tank holds 1 kg

const LIMITS = {
  name: 40,
  breed: 60,
  notes: 500,
  weight_kg: { min: 0.5, max: 100 },
  oldest_dog_years: 30,
};

const TIME_PATTERN = /^([01]\d|2[0-3]):[0-5]\d$/;
const MONTH_PATTERN = /^\d{4}-(0[1-9]|1[0-2])$/;
const DATE_PATTERN = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
const NUMBER_PATTERN = /^\d+(\.\d+)?$/;

// Returns a number, or null when the text is not a plain positive number.
// Accepts a comma as the decimal mark, as many phones type it.
export function parseNumber(raw) {
  const text = String(raw ?? "").trim().replace(",", ".");
  return NUMBER_PATTERN.test(text) ? Number(text) : null;
}

// today is the home's local date, written as YYYY-MM-DD.
export function validateDog(form, today) {
  const errors = {};

  const name = String(form.name ?? "").trim();
  if (!name) errors.name = "Enter the dog's name.";
  else if (name.length > LIMITS.name) errors.name = `Use at most ${LIMITS.name} characters.`;

  const breed = String(form.breed ?? "").trim();
  if (!breed) errors.breed = "Enter the breed, or Mixed.";
  else if (breed.length > LIMITS.breed) errors.breed = `Use at most ${LIMITS.breed} characters.`;

  if (!SEX_OPTIONS.includes(form.sex)) errors.sex = "Choose female or male.";
  if (form.neutered !== "yes" && form.neutered !== "no") errors.neutered = "Choose yes or no.";

  const birthMonth = String(form.birth_month ?? "").trim();
  const thisMonth = today.slice(0, 7);
  const oldestMonth = `${Number(today.slice(0, 4)) - LIMITS.oldest_dog_years}${today.slice(4, 7)}`;
  if (!MONTH_PATTERN.test(birthMonth)) errors.birth_month = "Choose the month of birth. An estimate is fine.";
  else if (birthMonth > thisMonth) errors.birth_month = "The month of birth cannot be in the future.";
  else if (birthMonth < oldestMonth) errors.birth_month = `Choose a month in the last ${LIMITS.oldest_dog_years} years.`;

  if (!ACTIVITY_LEVELS.includes(form.activity)) errors.activity = "Choose low, medium or high.";
  if (!BODY_CONDITIONS.includes(form.body_condition)) errors.body_condition = "Choose thin, ideal or overweight.";

  const weight = parseNumber(form.current_weight_kg);
  const { min: weightMin, max: weightMax } = LIMITS.weight_kg;
  if (weight === null || weight < weightMin || weight > weightMax) {
    errors.current_weight_kg = `Enter a weight from ${weightMin} to ${weightMax} kg.`;
  }

  const measuredOn = String(form.weight_measured_on ?? "").trim();
  if (!DATE_PATTERN.test(measuredOn)) errors.weight_measured_on = "Choose the day of this weight.";
  else if (measuredOn > today) errors.weight_measured_on = "This day cannot be in the future.";

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
          neutered: form.neutered === "yes",
          birth_month: birthMonth,
          activity: form.activity,
          body_condition: form.body_condition,
          current_weight_kg: weight,
          weight_measured_on: measuredOn,
          notes: notes || null,
        }
      : null,
  };
}

// Same labels as the feeding plan generator, chosen by the number of meals.
const MEAL_LABELS = {
  1: ["Dinner"],
  2: ["Breakfast", "Dinner"],
  3: ["Breakfast", "Lunch", "Dinner"],
  4: ["Breakfast", "Lunch", "Afternoon", "Dinner"],
};

// Returns one error object per row, in the order the rows were given.
// When everything is valid, value holds the meals sorted by time with their slot and label.
export function validateSchedule(rows) {
  const rowErrors = rows.map(() => ({}));
  let formError = "";

  if (rows.length < 1) formError = "Add at least one meal.";
  if (rows.length > MAX_MEALS_PER_DAY) formError = `A dog can have at most ${MAX_MEALS_PER_DAY} meals a day.`;

  const seenTimes = new Set();
  const meals = rows.map((row, index) => {
    const localTime = String(row.local_time ?? "").trim();
    if (!TIME_PATTERN.test(localTime)) rowErrors[index].local_time = "Choose a time.";
    else if (seenTimes.has(localTime)) rowErrors[index].local_time = "Another meal already uses this time.";
    seenTimes.add(localTime);

    const grams = parseNumber(row.grams);
    if (grams === null || grams < GRAM_STEP || grams > MAX_GRAMS_PER_MEAL) {
      rowErrors[index].grams = `Enter ${GRAM_STEP} to ${MAX_GRAMS_PER_MEAL} g.`;
    } else if (grams % GRAM_STEP !== 0) {
      rowErrors[index].grams = `Use a multiple of ${GRAM_STEP} g.`;
    }
    return { local_time: localTime, grams };
  });

  const ok = !formError && rowErrors.every((errors) => Object.keys(errors).length === 0);
  const labels = MEAL_LABELS[rows.length];
  return {
    ok,
    formError,
    rowErrors,
    value: ok
      ? [...meals]
          .sort((a, b) => a.local_time.localeCompare(b.local_time))
          .map((meal, index) => ({ slot: index + 1, label: labels[index], ...meal }))
      : null,
  };
}

const DEFAULT_TIMES = {
  1: ["18:00"],
  2: ["08:00", "18:00"],
  3: ["08:00", "13:00", "18:00"],
  4: ["08:00", "12:00", "15:30", "18:30"],
};

// Suggested meal times for a new schedule. The owner enters the grams.
export function defaultTimes(mealCount) {
  return DEFAULT_TIMES[mealCount] ?? DEFAULT_TIMES[2];
}

// A free time for a new row, preferring the usual meal times.
export function nextFreeTime(usedTimes) {
  const candidates = [...DEFAULT_TIMES[3], ...DEFAULT_TIMES[4]];
  return candidates.find((time) => !usedTimes.includes(time)) ?? "";
}
