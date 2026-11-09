import { describe, expect, it } from "vitest";
import { defaultTimes, nextFreeTime, parseNumber, validateDog, validateSchedule } from "./validation.js";

const goodDog = {
  name: " Biscuit ",
  breed: "Labrador",
  sex: "male",
  age_months: "24",
  weight_kg: "28,5",
  activity: "medium",
  meals_per_day: "2",
  notes: "",
};

describe("parseNumber", () => {
  it("reads plain numbers and comma decimals", () => {
    expect(parseNumber("12")).toBe(12);
    expect(parseNumber("12,5")).toBe(12.5);
    expect(parseNumber(" 7.25 ")).toBe(7.25);
  });

  it("rejects text, negatives, empty values and exponents", () => {
    for (const raw of ["abc", "-5", "", null, undefined, "1e3", "0x10"]) {
      expect(parseNumber(raw)).toBeNull();
    }
  });
});

describe("validateDog", () => {
  it("returns clean numeric values for the AI contract", () => {
    const result = validateDog(goodDog);
    expect(result.ok).toBe(true);
    expect(result.value).toEqual({
      name: "Biscuit",
      breed: "Labrador",
      sex: "male",
      age_months: 24,
      weight_kg: 28.5,
      activity: "medium",
      meals_per_day: 2,
      notes: "",
    });
  });

  it("rejects text in the age and weight fields", () => {
    const result = validateDog({ ...goodDog, age_months: "two years", weight_kg: "heavy" });
    expect(result.ok).toBe(false);
    expect(result.errors.age_months).toBeTruthy();
    expect(result.errors.weight_kg).toBeTruthy();
  });

  it("rejects a fractional age and out of range values", () => {
    expect(validateDog({ ...goodDog, age_months: "2.5" }).errors.age_months).toBeTruthy();
    expect(validateDog({ ...goodDog, age_months: "0" }).errors.age_months).toBeTruthy();
    expect(validateDog({ ...goodDog, weight_kg: "0" }).errors.weight_kg).toBeTruthy();
    expect(validateDog({ ...goodDog, weight_kg: "500" }).errors.weight_kg).toBeTruthy();
  });

  it("rejects activity values the feeding plan code would silently treat as medium", () => {
    expect(validateDog({ ...goodDog, activity: "HIGH" }).errors.activity).toBeTruthy();
    expect(validateDog({ ...goodDog, activity: "extreme" }).errors.activity).toBeTruthy();
  });

  it("rejects meal counts the feeding plan code would silently change", () => {
    expect(validateDog({ ...goodDog, meals_per_day: "5" }).errors.meals_per_day).toBeTruthy();
    expect(validateDog({ ...goodDog, meals_per_day: "0" }).errors.meals_per_day).toBeTruthy();
  });

  it("requires a name, a breed and a sex", () => {
    const { errors } = validateDog({ ...goodDog, name: "  ", breed: "", sex: "" });
    expect(Object.keys(errors).sort()).toEqual(["breed", "name", "sex"]);
  });
});

describe("validateSchedule", () => {
  it("accepts valid meals and sorts them by time", () => {
    const result = validateSchedule([
      { time: "18:00", grams: "280" },
      { time: "07:30", grams: 280 },
    ]);
    expect(result.ok).toBe(true);
    expect(result.value).toEqual([
      { time: "07:30", grams: 280 },
      { time: "18:00", grams: 280 },
    ]);
  });

  it("requires grams to be multiples of 5 within range", () => {
    const check = (grams) => validateSchedule([{ time: "07:30", grams }]).rowErrors[0].grams;
    expect(check("12")).toMatch(/multiple/);
    expect(check("0")).toBeTruthy();
    expect(check("1005")).toBeTruthy();
    expect(check("")).toBeTruthy();
    expect(check("5")).toBeUndefined();
    expect(check("1000")).toBeUndefined();
  });

  it("rejects invalid and duplicate times", () => {
    const result = validateSchedule([
      { time: "25:00", grams: "50" },
      { time: "08:00", grams: "50" },
      { time: "08:00", grams: "50" },
    ]);
    expect(result.rowErrors[0].time).toBeTruthy();
    expect(result.rowErrors[1].time).toBeUndefined();
    expect(result.rowErrors[2].time).toMatch(/already/);
  });

  it("allows 1 to 4 meals only", () => {
    expect(validateSchedule([]).ok).toBe(false);
    const five = ["06:00", "09:00", "12:00", "15:00", "18:00"].map((time) => ({ time, grams: "50" }));
    expect(validateSchedule(five).ok).toBe(false);
    expect(validateSchedule(five.slice(0, 4)).ok).toBe(true);
  });
});

describe("meal time helpers", () => {
  it("suggests one time per meal", () => {
    for (const count of [1, 2, 3, 4]) expect(defaultTimes(count)).toHaveLength(count);
  });

  it("offers a time that is not in use", () => {
    expect(["07:30"]).not.toContain(nextFreeTime(["07:30"]));
  });
});
