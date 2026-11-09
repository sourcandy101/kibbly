// Sample content for preview mode, used until Firebase and the feeder are linked.

import { clockTime } from "../logic/today_meals.js";

export const SAMPLE_HOME_ID = "home_sample";

export function makeSampleDogs() {
  const shared = { home_id: SAMPLE_HOME_ID, photo_urls: [], video_url: null, voice_clip_url: null };
  return [
    {
      ...shared,
      id: "dog_biscuit",
      name: "Biscuit",
      breed: "Labrador Retriever",
      sex: "male",
      age_months: 24,
      weight_kg: 28,
      activity: "medium",
      meals_per_day: 2,
      notes: "Shy, so he eats first.",
      call_order: 1,
    },
    {
      ...shared,
      id: "dog_mochi",
      name: "Mochi",
      breed: "French Bulldog",
      sex: "female",
      age_months: 36,
      weight_kg: 9,
      activity: "low",
      meals_per_day: 3,
      notes: "Tries to eat everyone's dinner.",
      call_order: 2,
    },
  ];
}

export function makeSampleSchedules() {
  return {
    dog_biscuit: {
      dog_id: "dog_biscuit",
      home_id: SAMPLE_HOME_ID,
      meals: [
        { time: "07:30", grams: 280 },
        { time: "18:00", grams: 280 },
      ],
    },
    dog_mochi: {
      dog_id: "dog_mochi",
      home_id: SAMPLE_HOME_ID,
      meals: [
        { time: "07:30", grams: 45 },
        { time: "12:30", grams: 45 },
        { time: "18:00", grams: 45 },
      ],
    },
  };
}

export function makeSampleHome(ownerId, now = new Date()) {
  return {
    id: SAMPLE_HOME_ID,
    owner_id: ownerId,
    feeder_id: "feeder_sample",
    wifi_status: "connected",
    last_seen: now.toISOString(),
    tank_level_percent: 62,
  };
}

// Pretends the feeder served every meal whose time has already passed today.
export function makeSampleMealLogs(dogs, schedules, now = new Date()) {
  const currentTime = clockTime(now);
  return dogs.flatMap((dog) =>
    (schedules[dog.id]?.meals ?? [])
      .filter((meal) => meal.time <= currentTime)
      .map((meal, index) => {
        const [hours, minutes] = meal.time.split(":").map(Number);
        const when = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes);
        return {
          id: `meal_${dog.id}_${meal.time}`,
          home_id: dog.home_id,
          dog_id: dog.id,
          scheduled_time: meal.time,
          time: when.toISOString(),
          grams_served: meal.grams,
          grams_eaten: index % 2 === 0 ? meal.grams : Math.max(0, meal.grams - 5),
          recognized: true,
          confidence: 0.94,
        };
      }),
  );
}
