import { beforeEach, describe, expect, it } from "vitest";
import {
  deleteDog,
  getCurrentUser,
  loadHomeData,
  resetSampleData,
  saveCallOrder,
  saveDog,
  saveSchedule,
  signIn,
  signOut,
} from "./store.js";

const newDog = {
  name: "Pip",
  breed: "Beagle",
  sex: "female",
  neutered: false,
  birth_month: "2026-07",
  activity: "high",
  body_condition: "ideal",
  current_weight_kg: 6,
  weight_measured_on: "2026-11-02",
  notes: null,
};

const meals = [{ slot: 1, label: "Dinner", local_time: "09:00", grams: 560 }];

beforeEach(async () => {
  await signOut();
  await resetSampleData();
});

describe("account", () => {
  it("signs in and out without storing a password", async () => {
    expect(await getCurrentUser()).toBeNull();
    const user = await signIn(" Owner@Example.com ");
    expect(user.email).toBe("Owner@Example.com");
    expect(user.id).toBe("user_owner_example_com");
    expect(JSON.stringify(await getCurrentUser())).not.toMatch(/password/i);
    expect((await loadHomeData()).home.owner_id).toBe(user.id);
    await signOut();
    expect(await getCurrentUser()).toBeNull();
  });
});

describe("dogs", () => {
  it("starts with the two sample dogs in calling order", async () => {
    const { dogs } = await loadHomeData();
    expect(dogs.map((dog) => dog.name)).toEqual(["Biscuit", "Mochi"]);
  });

  it("adds a new dog at the end of the calling order", async () => {
    const dog = await saveDog(newDog);
    expect(dog.call_order).toBe(3);
    expect(dog.home_id).toBeTruthy();
    expect((await loadHomeData()).dogs).toHaveLength(3);
  });

  it("allows at most 8 dogs, the limit in the schema", async () => {
    for (let count = 2; count < 8; count += 1) await saveDog(newDog);
    await expect(saveDog(newDog)).rejects.toThrow(/at most 8/);
  });

  it("edits a dog without changing its identity or order", async () => {
    await saveDog({ ...newDog, name: "Biscuit Jr" }, "dog_biscuit");
    const { dogs } = await loadHomeData();
    expect(dogs[0]).toMatchObject({ dog_id: "dog_biscuit", name: "Biscuit Jr", call_order: 1 });
  });

  it("removes everything belonging to a deleted dog and closes the order gap", async () => {
    await deleteDog("dog_biscuit");
    const { dogs, schedules, weights, meals: mealDocs } = await loadHomeData();
    expect(dogs.map((dog) => [dog.dog_id, dog.call_order])).toEqual([["dog_mochi", 1]]);
    expect(schedules.dog_biscuit).toBeUndefined();
    expect(weights.some((entry) => entry.dog_id === "dog_biscuit")).toBe(false);
    expect(mealDocs.some((meal) => meal.dog_id === "dog_biscuit")).toBe(false);
  });
});

describe("weights", () => {
  const entriesFor = async (dogId) => (await loadHomeData()).weights.filter((entry) => entry.dog_id === dogId);
  const biscuit = async () => (await loadHomeData()).dogs.find((dog) => dog.dog_id === "dog_biscuit");

  it("creates the first weigh in with a new dog", async () => {
    const dog = await saveDog(newDog);
    const entries = await entriesFor(dog.dog_id);
    expect(entries).toHaveLength(1);
    expect(entries[0]).toMatchObject({ weight_kg: 6, measured_on: "2026-11-02" });
  });

  it("adds a weigh in when the weight changes and copies it to the profile", async () => {
    await saveDog({ ...newDog, current_weight_kg: 29, weight_measured_on: "2026-11-05" }, "dog_biscuit");
    expect(await entriesFor("dog_biscuit")).toHaveLength(2);
    expect(await biscuit()).toMatchObject({ current_weight_kg: 29, weight_measured_on: "2026-11-05" });
  });

  it("adds nothing when the weight is unchanged", async () => {
    const dog = await biscuit();
    await saveDog({ ...newDog, current_weight_kg: dog.current_weight_kg, weight_measured_on: dog.weight_measured_on }, "dog_biscuit");
    expect(await entriesFor("dog_biscuit")).toHaveLength(1);
  });

  it("keeps the newest weight as current when an older one is added", async () => {
    await saveDog({ ...newDog, current_weight_kg: 25, weight_measured_on: "2026-01-01" }, "dog_biscuit");
    expect(await entriesFor("dog_biscuit")).toHaveLength(2);
    expect(await biscuit()).toMatchObject({ current_weight_kg: 28, weight_measured_on: "2026-11-01" });
  });
});

describe("schedules", () => {
  it("saves the meals with their daily total", async () => {
    await saveSchedule("dog_biscuit", meals);
    const { dogs, schedules } = await loadHomeData();
    expect(schedules.dog_biscuit.meals).toEqual(meals);
    expect(schedules.dog_biscuit.daily_total_grams).toBe(560);
    expect(schedules.dog_biscuit.plan_source).toBe("owner_edited");
    expect(schedules.dog_biscuit.home_id).toBe(dogs[0].home_id);
  });

  it("fails clearly for a dog that does not exist", async () => {
    await expect(saveSchedule("missing", [])).rejects.toThrow(/no longer exists/);
  });
});

describe("calling order", () => {
  it("saves a new order", async () => {
    await saveCallOrder(["dog_mochi", "dog_biscuit"]);
    const { dogs } = await loadHomeData();
    expect(dogs.map((dog) => [dog.name, dog.call_order])).toEqual([
      ["Mochi", 1],
      ["Biscuit", 2],
    ]);
  });
});
