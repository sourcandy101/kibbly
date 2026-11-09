// Time rules from schemas/README.md: moments are UTC with whole seconds,
// schedules use the local clock of the home, and age is computed from birth_month.

function partsIn(date, timezone) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: timezone,
    hourCycle: "h23",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  }).formatToParts(date);
  return Object.fromEntries(parts.map((part) => [part.type, part.value]));
}

export function deviceTimezone() {
  return Intl.DateTimeFormat().resolvedOptions().timeZone || "Africa/Tunis";
}

export function utcStamp(date = new Date()) {
  return date.toISOString().replace(/\.\d{3}Z$/, "Z");
}

export function localDateIn(date, timezone) {
  const { year, month, day } = partsIn(date, timezone);
  return `${year}-${month}-${day}`;
}

export function localTimeIn(date, timezone) {
  const { hour, minute } = partsIn(date, timezone);
  return `${hour}:${minute}`;
}

function offsetMs(date, timezone) {
  const { year, month, day, hour, minute, second } = partsIn(date, timezone);
  const wall = Date.UTC(Number(year), Number(month) - 1, Number(day), Number(hour), Number(minute), Number(second));
  return wall - Math.floor(date.getTime() / 1000) * 1000;
}

// The moment when a home's clock shows this date and time.
export function localToUtc(localDate, localTime, timezone) {
  const [year, month, day] = localDate.split("-").map(Number);
  const [hour, minute] = localTime.split(":").map(Number);
  const wall = Date.UTC(year, month - 1, day, hour, minute);
  const firstGuess = wall - offsetMs(new Date(wall), timezone);
  return new Date(wall - offsetMs(new Date(firstGuess), timezone));
}

export function ageInMonths(birthMonth, today) {
  const [birthYear, birth] = birthMonth.split("-").map(Number);
  const [year, month] = today.split("-").map(Number);
  return Math.max(0, (year - birthYear) * 12 + (month - birth));
}

export function ageLabel(birthMonth, today) {
  const months = ageInMonths(birthMonth, today);
  if (months < 1) return "under 1 month";
  if (months < 24) return `${months} ${months === 1 ? "month" : "months"}`;
  return `${Math.floor(months / 12)} years`;
}
