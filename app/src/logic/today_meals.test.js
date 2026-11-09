import { describe, expect, it } from "vitest";
import { buildTodayMeals, summarizeToday } from "./today_meals.js";

const now = new Date(2026, 10, 9, 13, 0);
const dogs = [
  { id: "mochi", name: "Mochi", call_order: 2 },
  { id: "biscuit", name: "Biscuit", call_order: 1 },
];
const schedules = {
  biscuit: { meals: [{ time: "07:30", grams: 280 }, { time: "18:00", grams: 280 }] },
  mochi: { meals: [{ time: "07:30", grams: 45 }, { time: "12:30", grams: 45 }] },
};
const logs = [
  {
    dog_id: "biscuit",
    scheduled_time: "07:30",
    time: new Date(2026, 10, 9, 7, 31).toISOString(),
    grams_served: 280,
    grams_eaten: 275,
  },
];

describe("buildTodayMeals", () => {
  it("sorts by time, then by calling order", () => {
    const rows = buildTodayMeals(dogs, schedules, logs, now);
    expect(rows.map((row) => row.key)).toEqual([
      "biscuit_07:30",
      "mochi_07:30",
      "mochi_12:30",
      "biscuit_18:00",
    ]);
  });

  it("marks meals as done, no report or upcoming", () => {
    const rows = buildTodayMeals(dogs, schedules, logs, now);
    expect(rows.map((row) => row.status)).toEqual(["done", "no_report", "no_report", "upcoming"]);
  });

  it("ignores logs from another day", () => {
    const yesterday = [{ ...logs[0], time: new Date(2026, 10, 8, 7, 31).toISOString() }];
    expect(buildTodayMeals(dogs, schedules, yesterday, now)[0].status).toBe("no_report");
  });

  it("handles a dog with no schedule", () => {
    expect(buildTodayMeals([{ id: "new", name: "New", call_order: 1 }], {}, [], now)).toEqual([]);
  });
});

describe("summarizeToday", () => {
  it("adds planned and eaten grams", () => {
    const rows = buildTodayMeals(dogs, schedules, logs, now);
    expect(summarizeToday(rows)).toEqual({ planned_grams: 650, eaten_grams: 275 });
  });
});
