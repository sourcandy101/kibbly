// Combines schedules and meal documents into the list shown on the home screen.

import { localDateIn, localTimeIn } from "./time.js";

// A row's status is the meal document's status from schemas/meal.json, or one of:
//   upcoming   the meal time has not arrived
//   no_report  the meal time passed and the feeder has not reported yet
export function buildTodayMeals(dogs, schedules, mealDocs, timezone, now = new Date()) {
  const today = localDateIn(now, timezone);
  const currentTime = localTimeIn(now, timezone);
  const todayDocs = mealDocs.filter((doc) => localDateIn(new Date(doc.scheduled_at), timezone) === today);

  const rows = dogs.flatMap((dog) =>
    (schedules[dog.dog_id]?.meals ?? []).map((meal) => {
      const doc = todayDocs.find((entry) => entry.dog_id === dog.dog_id && entry.slot === meal.slot);
      let status = "no_report";
      if (doc) status = doc.status;
      else if (meal.local_time > currentTime) status = "upcoming";
      return {
        key: `${dog.dog_id}_${meal.slot}`,
        dog_id: dog.dog_id,
        dog_name: dog.name,
        call_order: dog.call_order,
        label: meal.label,
        local_time: meal.local_time,
        planned_grams: meal.grams,
        grams_dispensed: doc?.grams_dispensed ?? null,
        grams_eaten: doc?.grams_eaten ?? null,
        status,
      };
    }),
  );

  return rows.sort((a, b) => a.local_time.localeCompare(b.local_time) || a.call_order - b.call_order);
}

export function summarizeToday(rows) {
  return {
    planned_grams: rows.reduce((sum, row) => sum + row.planned_grams, 0),
    eaten_grams: rows.reduce((sum, row) => sum + (row.grams_eaten ?? 0), 0),
  };
}
