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
  age_months: 4,
  weight_kg: 6,
  activity: "high",
  meals_per_day: 4,
  notes: "",
};

beforeEach(async () => {
  await signOut();
  await resetSampleData();
});

describe("account", () => {
  it("signs in and out without storing a password", async () => {
    expect(await getCurrentUser()).toBeNull();
    const user = await signIn(" Owner@Example.com ");
    expect(user.email).toBe("Owner@Example.com");
    expect(JSON.stringify(await getCurrentUser())).not.toMatch(/password/i);
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

  it("edits a dog without changing its identity or order", async () => {
    await saveDog({ ...newDog, name: "Biscuit Jr" }, "dog_biscuit");
    const { dogs } = await loadHomeData();
    expect(dogs[0]).toMatchObject({ id: "dog_biscuit", name: "Biscuit Jr", call_order: 1 });
  });

  it("removes the schedule and meals of a deleted dog and closes the order gap", async () => {
    await deleteDog("dog_biscuit");
    const { dogs, schedules, meals } = await loadHomeData();
    expect(dogs.map((dog) => [dog.id, dog.call_order])).toEqual([["dog_mochi", 1]]);
    expect(schedules.dog_biscuit).toBeUndefined();
    expect(meals.some((meal) => meal.dog_id === "dog_biscuit")).toBe(false);
  });
});

describe("schedules", () => {
  it("keeps meals_per_day equal to the saved meal count", async () => {
    await saveSchedule("dog_biscuit", [{ time: "09:00", grams: 560 }]);
    const { dogs, schedules } = await loadHomeData();
    expect(dogs[0].meals_per_day).toBe(1);
    expect(schedules.dog_biscuit.meals).toEqual([{ time: "09:00", grams: 560 }]);
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
