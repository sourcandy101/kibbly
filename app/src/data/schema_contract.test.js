// Checks what the app saves against the team's data contract in schemas/,
// so the app cannot drift away from the feeder and the AI server unnoticed.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { validateDog, validateSchedule } from "../logic/validation.js";
import { makeSampleDogs, makeSampleHome, makeSampleMeals, makeSampleSchedules } from "./sample_data.js";
import { loadHomeData, resetSampleData, saveCallOrder, saveDog, saveSchedule, signIn } from "./store.js";

const SCHEMA_FOLDER = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../schemas");

const ajv = new Ajv2020({ strict: false, allErrors: true });
const schemaIds = {};
for (const file of fs.readdirSync(SCHEMA_FOLDER).filter((name) => name.endsWith(".json"))) {
  const schema = JSON.parse(fs.readFileSync(path.join(SCHEMA_FOLDER, file), "utf8"));
  ajv.addSchema(schema);
  schemaIds[file.replace(".json", "")] = schema.$id;
}

function problems(schemaName, document) {
  const validate = ajv.getSchema(schemaIds[schemaName]);
  return validate(document) ? [] : validate.errors.map((error) => `${error.instancePath} ${error.message}`);
}

const form = {
  name: "Pip",
  breed: "Beagle",
  sex: "female",
  neutered: "no",
  birth_month: "2025-09",
  activity: "high",
  body_condition: "ideal",
  current_weight_kg: "12,5",
  weight_measured_on: "2026-11-02",
  notes: "",
};

async function expectAllValid() {
  const { home, dogs, schedules, weights, meals } = await loadHomeData();
  expect(problems("home", home)).toEqual([]);
  for (const dog of dogs) expect(problems("dog", dog)).toEqual([]);
  for (const schedule of Object.values(schedules)) expect(problems("schedule", schedule)).toEqual([]);
  for (const entry of weights) expect(problems("weight_entry", entry)).toEqual([]);
  for (const meal of meals) expect(problems("meal", meal)).toEqual([]);
}

describe("data contract", () => {
  beforeEach(async () => {
    await resetSampleData();
  });

  it("the checker itself rejects bad documents", () => {
    expect(problems("dog", { name: "Only a name" })).not.toHaveLength(0);
  });

  it("sample home and served meals are valid late in the day, when every meal has been served", () => {
    vi.setSystemTime(new Date("2026-11-09T22:00:00Z"));
    const now = new Date();
    const timezone = "Africa/Tunis";
    const dogs = makeSampleDogs(now);
    const schedules = makeSampleSchedules(now);
    const meals = makeSampleMeals(dogs, schedules, timezone, now);
    vi.useRealTimers();
    expect(meals.length).toBeGreaterThan(0);
    expect(problems("home", makeSampleHome("user_sample", timezone, now))).toEqual([]);
    for (const meal of meals) expect(problems("meal", meal)).toEqual([]);
  });

  it("documents stay valid after signing in with any email", async () => {
    await signIn("first.last+test@example.com");
    await expectAllValid();
  });

  it("a dog and schedule from the forms are valid, including every optional path", async () => {
    const dog = validateDog(form, "2026-11-09").value;
    const saved = await saveDog(dog);
    const meals = validateSchedule([
      { local_time: "18:00", grams: "100" },
      { local_time: "08:00", grams: "100" },
      { local_time: "12:30", grams: "100" },
      { local_time: "15:00", grams: "100" },
    ]).value;
    await saveSchedule(saved.dog_id, meals);
    await saveDog({ ...dog, notes: "Shy", current_weight_kg: 13, weight_measured_on: "2026-11-05" }, saved.dog_id);
    await saveCallOrder([saved.dog_id]);
    await expectAllValid();
  });
});
