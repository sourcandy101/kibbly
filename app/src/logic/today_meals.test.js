import { describe, expect, it } from "vitest";
import { buildTodayMeals, summarizeToday } from "./today_meals.js";

const TIMEZONE = "Africa/Tunis";
const now = new Date("2026-11-09T12:00:00Z"); // 13:00 in Tunis

const dogs = [
  { dog_id: "dog_mochi", name: "Mochi", call_order: 2 },
  { dog_id: "dog_biscuit", name: "Biscuit", call_order: 1 },
];
const schedules = {
  dog_biscuit: {
    meals: [
      { slot: 1, label: "Breakfast", local_time: "08:00", grams: 280 },
      { slot: 2, label: "Dinner", local_time: "18:00", grams: 280 },
    ],
  },
  dog_mochi: {
    meals: [
      { slot: 1, label: "Breakfast", local_time: "08:00", grams: 45 },
      { slot: 2, label: "Lunch", local_time: "12:30", grams: 45 },
    ],
  },
};
const docs = [
  {
    dog_id: "dog_biscuit",
    slot: 1,
    scheduled_at: "2026-11-09T07:00:00Z",
    status: "completed",
    grams_dispensed: 280,
    grams_eaten: 275,
  },
];

describe("buildTodayMeals", () => {
  it("sorts by time, then by calling order", () => {
    const rows = buildTodayMeals(dogs, schedules, docs, TIMEZONE, now);
    expect(rows.map((row) => row.key)).toEqual(["dog_biscuit_1", "dog_mochi_1", "dog_mochi_2", "dog_biscuit_2"]);
  });

  it("uses the meal status, or no report and upcoming when there is no document", () => {
    const rows = buildTodayMeals(dogs, schedules, docs, TIMEZONE, now);
    expect(rows.map((row) => row.status)).toEqual(["completed", "no_report", "no_report", "upcoming"]);
  });

  it("shows failed meals with their own status", () => {
    const missed = [{ ...docs[0], status: "missed_no_show", grams_dispensed: 0, grams_eaten: 0 }];
    expect(buildTodayMeals(dogs, schedules, missed, TIMEZONE, now)[0].status).toBe("missed_no_show");
  });

  it("ignores documents from another day", () => {
    const yesterday = [{ ...docs[0], scheduled_at: "2026-11-08T07:00:00Z" }];
    expect(buildTodayMeals(dogs, schedules, yesterday, TIMEZONE, now)[0].status).toBe("no_report");
  });

  it("decides today by the clock of the home, not by UTC", () => {
    const lateNight = new Date("2026-11-09T23:30:00Z"); // already 10 November in Tunis
    const rows = buildTodayMeals(dogs, schedules, docs, TIMEZONE, lateNight);
    expect(rows[0].status).toBe("upcoming");
  });

  it("handles a dog with no schedule", () => {
    expect(buildTodayMeals([{ dog_id: "new", name: "New", call_order: 1 }], {}, [], TIMEZONE, now)).toEqual([]);
  });
});

describe("summarizeToday", () => {
  it("adds planned and eaten grams", () => {
    const rows = buildTodayMeals(dogs, schedules, docs, TIMEZONE, now);
    expect(summarizeToday(rows)).toEqual({ planned_grams: 650, eaten_grams: 275 });
  });
});
