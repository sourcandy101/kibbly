import { describe, expect, it } from "vitest";
import { ageInMonths, ageLabel, localDateIn, localTimeIn, localToUtc, utcStamp } from "./time.js";

describe("utcStamp", () => {
  it("uses UTC with whole seconds, as the schemas require", () => {
    expect(utcStamp(new Date("2026-11-09T07:00:00.123Z"))).toBe("2026-11-09T07:00:00Z");
  });
});

describe("home timezone", () => {
  const moment = new Date("2026-11-09T23:30:00Z");

  it("reads the local date and clock of the home", () => {
    expect(localDateIn(moment, "Africa/Tunis")).toBe("2026-11-10");
    expect(localTimeIn(moment, "Africa/Tunis")).toBe("00:30");
    expect(localDateIn(moment, "America/New_York")).toBe("2026-11-09");
  });

  it("matches the schema example: 08:00 in Tunis is 07:00 UTC", () => {
    expect(utcStamp(localToUtc("2026-11-09", "08:00", "Africa/Tunis"))).toBe("2026-11-09T07:00:00Z");
  });

  it("handles a zone behind UTC and summer time", () => {
    expect(utcStamp(localToUtc("2026-01-15", "08:00", "America/New_York"))).toBe("2026-01-15T13:00:00Z");
    expect(utcStamp(localToUtc("2026-07-15", "08:00", "America/New_York"))).toBe("2026-07-15T12:00:00Z");
  });
});

describe("age from birth_month", () => {
  it("computes months", () => {
    expect(ageInMonths("2024-03", "2026-11-09")).toBe(32);
    expect(ageInMonths("2026-11", "2026-11-09")).toBe(0);
  });

  it("writes a readable age", () => {
    expect(ageLabel("2026-11", "2026-11-09")).toBe("under 1 month");
    expect(ageLabel("2026-10", "2026-11-09")).toBe("1 month");
    expect(ageLabel("2025-09", "2026-11-09")).toBe("14 months");
    expect(ageLabel("2024-03", "2026-11-09")).toBe("2 years");
  });
});
