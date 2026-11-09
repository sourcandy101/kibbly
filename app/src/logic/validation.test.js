import { describe, expect, it } from "vitest";
import { defaultTimes, nextFreeTime, parseNumber, validateDog, validateSchedule } from "./validation.js";

const TODAY = "2026-11-09";

const goodDog = {
  name: " Biscuit ",
  breed: "Labrador",
  sex: "male",
  neutered: "yes",
  birth_month: "2024-03",
  activity: "medium",
  body_condition: "ideal",
  current_weight_kg: "28,5",
  weight_measured_on: "2026-11-01",
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
  it("returns clean values with the schema field names", () => {
    const result = validateDog(goodDog, TODAY);
    expect(result.ok).toBe(true);
    expect(result.value).toEqual({
      name: "Biscuit",
      breed: "Labrador",
      sex: "male",
      neutered: true,
      birth_month: "2024-03",
      activity: "medium",
      body_condition: "ideal",
      current_weight_kg: 28.5,
      weight_measured_on: "2026-11-01",
      notes: null,
    });
  });

  it("rejects text in the weight field and out of range weights", () => {
    expect(validateDog({ ...goodDog, current_weight_kg: "heavy" }, TODAY).errors.current_weight_kg).toBeTruthy();
    expect(validateDog({ ...goodDog, current_weight_kg: "0" }, TODAY).errors.current_weight_kg).toBeTruthy();
    expect(validateDog({ ...goodDog, current_weight_kg: "101" }, TODAY).errors.current_weight_kg).toBeTruthy();
  });

  it("checks the birth month", () => {
    const check = (birth_month) => validateDog({ ...goodDog, birth_month }, TODAY).errors.birth_month;
    expect(check("")).toBeTruthy();
    expect(check("2024-13")).toBeTruthy();
    expect(check("2026-12")).toMatch(/future/);
    expect(check("1990-01")).toBeTruthy();
    expect(check("2026-11")).toBeUndefined();
  });

  it("rejects a weigh in dated in the future", () => {
    expect(validateDog({ ...goodDog, weight_measured_on: "2026-11-10" }, TODAY).errors.weight_measured_on).toMatch(/future/);
    expect(validateDog({ ...goodDog, weight_measured_on: TODAY }, TODAY).errors.weight_measured_on).toBeUndefined();
  });

  it("rejects values outside the schema lists", () => {
    expect(validateDog({ ...goodDog, activity: "HIGH" }, TODAY).errors.activity).toBeTruthy();
    expect(validateDog({ ...goodDog, body_condition: "chubby" }, TODAY).errors.body_condition).toBeTruthy();
    expect(validateDog({ ...goodDog, sex: "unknown" }, TODAY).errors.sex).toBeTruthy();
  });

  it("requires every required choice", () => {
    const { errors } = validateDog({ ...goodDog, name: "  ", breed: "", neutered: "", body_condition: "" }, TODAY);
    expect(Object.keys(errors).sort()).toEqual(["body_condition", "breed", "name", "neutered"]);
  });

  it("keeps notes when given", () => {
    expect(validateDog({ ...goodDog, notes: " Shy " }, TODAY).value.notes).toBe("Shy");
  });
});

describe("validateSchedule", () => {
  it("sorts by time and adds slots and labels", () => {
    const result = validateSchedule([
      { local_time: "18:00", grams: "280" },
      { local_time: "08:00", grams: 280 },
    ]);
    expect(result.ok).toBe(true);
    expect(result.value).toEqual([
      { slot: 1, label: "Breakfast", local_time: "08:00", grams: 280 },
      { slot: 2, label: "Dinner", local_time: "18:00", grams: 280 },
    ]);
  });

  it("requires grams to be multiples of 5 within range", () => {
    const check = (grams) => validateSchedule([{ local_time: "08:00", grams }]).rowErrors[0].grams;
    expect(check("12")).toMatch(/multiple/);
    expect(check("0")).toBeTruthy();
    expect(check("1005")).toBeTruthy();
    expect(check("")).toBeTruthy();
    expect(check("5")).toBeUndefined();
    expect(check("1000")).toBeUndefined();
  });

  it("rejects invalid and duplicate times", () => {
    const result = validateSchedule([
      { local_time: "25:00", grams: "50" },
      { local_time: "08:00", grams: "50" },
      { local_time: "08:00", grams: "50" },
    ]);
    expect(result.rowErrors[0].local_time).toBeTruthy();
    expect(result.rowErrors[1].local_time).toBeUndefined();
    expect(result.rowErrors[2].local_time).toMatch(/already/);
  });

  it("allows 1 to 4 meals only", () => {
    expect(validateSchedule([]).ok).toBe(false);
    const five = ["06:00", "09:00", "12:00", "15:00", "18:00"].map((local_time) => ({ local_time, grams: "50" }));
    expect(validateSchedule(five).ok).toBe(false);
    expect(validateSchedule(five.slice(0, 4)).ok).toBe(true);
    expect(validateSchedule(five.slice(0, 4)).value.map((meal) => meal.label)).toEqual([
      "Breakfast",
      "Lunch",
      "Afternoon",
      "Dinner",
    ]);
  });
});

describe("meal time helpers", () => {
  it("suggests one time per meal", () => {
    for (const count of [1, 2, 3, 4]) expect(defaultTimes(count)).toHaveLength(count);
  });

  it("offers a time that is not in use", () => {
    expect(nextFreeTime(["08:00"])).not.toBe("08:00");
    expect(nextFreeTime(["08:00", "13:00", "18:00"])).toBe("12:00");
  });
});
