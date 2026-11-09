// Sample documents for preview mode, in the exact shape of schemas/.
// Used until Firebase and the feeder are linked.

import { localDateIn, localTimeIn, localToUtc, utcStamp } from "../logic/time.js";

export const SAMPLE_HOME_ID = "home_sample";
const SAMPLE_WEIGHED_ON = "2026-11-01";

export function emptyMedia() {
  return { photo_urls: [], video_url: null, voice_clip_url: null };
}

export function emptyRecognition() {
  return { status: "not_enrolled", reference_images: 0, updated_at: null };
}

export function makeSampleHome(ownerId, timezone, now = new Date()) {
  return {
    home_id: SAMPLE_HOME_ID,
    owner_id: ownerId,
    timezone,
    kibble: { brand: null, kcal_per_kg: null },
    feeder: {
      feeder_id: "feeder_sample",
      wifi_status: "online",
      last_seen_at: utcStamp(now),
      tank_capacity_grams: 1000,
      tank_grams_estimate: 620,
    },
    created_at: utcStamp(now),
  };
}

export function makeSampleDogs(now = new Date()) {
  const shared = {
    home_id: SAMPLE_HOME_ID,
    weight_measured_on: SAMPLE_WEIGHED_ON,
    media: emptyMedia(),
    recognition: emptyRecognition(),
    created_at: utcStamp(now),
    updated_at: utcStamp(now),
  };
  return [
    {
      ...shared,
      dog_id: "dog_biscuit",
      name: "Biscuit",
      breed: "Labrador Retriever",
      sex: "male",
      neutered: true,
      birth_month: "2024-03",
      activity: "medium",
      body_condition: "ideal",
      current_weight_kg: 28,
      notes: "Shy, eats slowly.",
      call_order: 1,
    },
    {
      ...shared,
      dog_id: "dog_mochi",
      name: "Mochi",
      breed: "French Bulldog",
      sex: "female",
      neutered: true,
      birth_month: "2023-06",
      activity: "low",
      body_condition: "overweight",
      current_weight_kg: 9,
      notes: "Tries to eat everyone's dinner.",
      call_order: 2,
    },
  ];
}

export function makeSampleWeights(dogs, now = new Date()) {
  return dogs.map((dog) => ({
    weight_id: `weight_${dog.dog_id}`,
    home_id: dog.home_id,
    dog_id: dog.dog_id,
    measured_on: dog.weight_measured_on,
    weight_kg: dog.current_weight_kg,
    entered_at: utcStamp(now),
  }));
}

function makeSampleSchedule(dogId, meals, now) {
  return {
    dog_id: dogId,
    home_id: SAMPLE_HOME_ID,
    meals,
    daily_total_grams: meals.reduce((sum, meal) => sum + meal.grams, 0),
    plan_source: "owner_edited",
    confirmed_at: utcStamp(now),
  };
}

export function makeSampleSchedules(now = new Date()) {
  return {
    dog_biscuit: makeSampleSchedule(
      "dog_biscuit",
      [
        { slot: 1, label: "Breakfast", local_time: "08:00", grams: 280 },
        { slot: 2, label: "Dinner", local_time: "18:00", grams: 280 },
      ],
      now,
    ),
    dog_mochi: makeSampleSchedule(
      "dog_mochi",
      [
        { slot: 1, label: "Breakfast", local_time: "08:00", grams: 45 },
        { slot: 2, label: "Lunch", local_time: "13:00", grams: 45 },
        { slot: 3, label: "Dinner", local_time: "18:00", grams: 45 },
      ],
      now,
    ),
  };
}

function plusMinutes(date, minutes) {
  return new Date(date.getTime() + minutes * 60000);
}

// Pretends the feeder served every meal whose time has already passed today.
export function makeSampleMeals(dogs, schedules, timezone, now = new Date()) {
  const today = localDateIn(now, timezone);
  const currentTime = localTimeIn(now, timezone);
  const dayId = today.replaceAll("-", "");

  return dogs.flatMap((dog) =>
    (schedules[dog.dog_id]?.meals ?? [])
      .filter((meal) => meal.local_time <= currentTime)
      .map((meal) => {
        const scheduledAt = localToUtc(today, meal.local_time, timezone);
        const arrivedAt = utcStamp(plusMinutes(scheduledAt, 1));
        const endedAt = utcStamp(plusMinutes(scheduledAt, 5));
        const gramsEaten = meal.slot % 2 === 0 ? Math.max(0, meal.grams - 5) : meal.grams;
        return {
          meal_id: `meal_${dog.dog_id}_${meal.slot}_${dayId}`,
          home_id: dog.home_id,
          dog_id: dog.dog_id,
          slot: meal.slot,
          scheduled_at: utcStamp(scheduledAt),
          planned_grams: meal.grams,
          status: "completed",
          recognition_mode: "camera",
          call_attempts: 1,
          first_arrival_at: arrivedAt,
          ended_at: endedAt,
          bowl_grams_at_start: 0,
          grams_dispensed: meal.grams,
          grams_eaten: gramsEaten,
          grams_left_in_bowl: meal.grams - gramsEaten,
          visits: [
            {
              visit_id: `visit_${dog.dog_id}_${meal.slot}_${dayId}`,
              started_at: arrivedAt,
              ended_at: endedAt,
              classification: "known_dog",
              dog_id: dog.dog_id,
              confidence: 0.94,
              outcome: "served",
              grams_dispensed: meal.grams,
              grams_eaten: gramsEaten,
              photo_url: null,
            },
          ],
          logged_offline: false,
        };
      }),
  );
}
