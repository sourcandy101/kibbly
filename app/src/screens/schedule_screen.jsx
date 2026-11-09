import { useRef, useState } from "react";
import { saveSchedule } from "../data/store.js";
import { go, pathTo } from "../logic/routes.js";
import {
  GRAM_STEP,
  MAX_GRAMS_PER_MEAL,
  MAX_MEALS_PER_DAY,
  defaultTimes,
  nextFreeTime,
  parseNumber,
  validateSchedule,
} from "../logic/validation.js";

// Rows start from the saved schedule. When the profile asks for more meals than
// are saved, empty rows are added. Extra saved meals are kept for the owner to
// remove, so no meal is ever dropped silently.
function initialRows(dog, schedule) {
  const saved = schedule?.meals ?? [];
  const rows = saved.map((meal) => ({ time: meal.time, grams: String(meal.grams) }));
  if (saved.length === 0) {
    return defaultTimes(dog.meals_per_day).map((time) => ({ time, grams: "" }));
  }
  while (rows.length < dog.meals_per_day) {
    rows.push({ time: nextFreeTime(rows.map((row) => row.time)), grams: "" });
  }
  return rows;
}

function stepGrams(current, direction) {
  const value = parseNumber(current) ?? 0;
  const snapped = direction > 0 ? Math.floor(value / GRAM_STEP) * GRAM_STEP + GRAM_STEP : Math.ceil(value / GRAM_STEP) * GRAM_STEP - GRAM_STEP;
  return String(Math.min(MAX_GRAMS_PER_MEAL, Math.max(GRAM_STEP, snapped)));
}

export default function ScheduleScreen({ data, refresh, dogId }) {
  const dog = data.dogs.find((entry) => entry.id === dogId);
  const schedule = data.schedules[dogId];
  const nextRowId = useRef(0);
  const withId = (row) => ({ ...row, id: nextRowId.current++ });

  const [rows, setRows] = useState(() => (dog ? initialRows(dog, schedule).map(withId) : []));
  const [validation, setValidation] = useState(null);
  const [saveError, setSaveError] = useState("");

  if (!dog) {
    return (
      <div className="card empty">
        <p>This dog no longer exists.</p>
        <a className="button" href={pathTo("dogs")}>
          Back to dogs
        </a>
      </div>
    );
  }

  const updateRow = (id, field, value) => {
    setRows((current) => current.map((row) => (row.id === id ? { ...row, [field]: value } : row)));
    setValidation(null);
  };

  const addRow = () => {
    setRows((current) => [...current, withId({ time: nextFreeTime(current.map((row) => row.time)), grams: "" })]);
    setValidation(null);
  };

  const removeRow = (id) => {
    setRows((current) => current.filter((row) => row.id !== id));
    setValidation(null);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const result = validateSchedule(rows);
    setValidation(result);
    setSaveError("");
    if (!result.ok) return;
    try {
      await saveSchedule(dogId, result.value);
      await refresh();
      go("dogs");
    } catch (error) {
      setSaveError(error.message);
    }
  };

  const dailyTotal = rows.reduce((sum, row) => sum + (parseNumber(row.grams) ?? 0), 0);
  const extraMeals = rows.length - dog.meals_per_day;

  return (
    <>
      <header className="page_header">
        <h1>{dog.name}'s meals</h1>
        <a className="button" href={pathTo("dogs")}>
          Cancel
        </a>
      </header>

      {extraMeals > 0 && (
        <p className="notice">
          The profile says {dog.meals_per_day} {dog.meals_per_day === 1 ? "meal" : "meals"} a day, but this schedule has{" "}
          {rows.length}. Remove any you no longer want. Saving updates the profile to match.
        </p>
      )}

      <form onSubmit={handleSubmit} noValidate>
        <ul className="schedule_list">
          {rows.map((row, index) => {
            const errors = validation?.rowErrors[index] ?? {};
            return (
              <li key={row.id} className="card schedule_row">
                <div className="schedule_row_top">
                  <h2>Meal {index + 1}</h2>
                  {rows.length > 1 && (
                    <button
                      type="button"
                      className="link_button"
                      onClick={() => removeRow(row.id)}
                      aria-label={`Remove meal ${index + 1}`}
                    >
                      Remove
                    </button>
                  )}
                </div>
                <div className="schedule_fields">
                  <div className="field">
                    <label htmlFor={`time_${row.id}`}>Time</label>
                    <input
                      id={`time_${row.id}`}
                      type="time"
                      value={row.time}
                      onChange={(event) => updateRow(row.id, "time", event.target.value)}
                      aria-invalid={errors.time ? true : undefined}
                    />
                    {errors.time && <p className="field_error">{errors.time}</p>}
                  </div>
                  <div className="field">
                    <label htmlFor={`grams_${row.id}`}>Grams</label>
                    <div className="stepper">
                      <button
                        type="button"
                        onClick={() => updateRow(row.id, "grams", stepGrams(row.grams, -1))}
                        aria-label={`${GRAM_STEP} grams less for meal ${index + 1}`}
                      >
                        −
                      </button>
                      <input
                        id={`grams_${row.id}`}
                        inputMode="numeric"
                        value={row.grams}
                        onChange={(event) => updateRow(row.id, "grams", event.target.value)}
                        aria-invalid={errors.grams ? true : undefined}
                        autoComplete="off"
                      />
                      <button
                        type="button"
                        onClick={() => updateRow(row.id, "grams", stepGrams(row.grams, 1))}
                        aria-label={`${GRAM_STEP} grams more for meal ${index + 1}`}
                      >
                        +
                      </button>
                    </div>
                    {errors.grams && <p className="field_error">{errors.grams}</p>}
                  </div>
                </div>
              </li>
            );
          })}
        </ul>

        {rows.length < MAX_MEALS_PER_DAY && (
          <button type="button" className="button button_wide" onClick={addRow}>
            Add a meal
          </button>
        )}

        <p className="schedule_total">
          Daily total: <strong>{dailyTotal} g</strong>
        </p>

        {validation?.formError && (
          <p className="field_error" role="alert">
            {validation.formError}
          </p>
        )}
        {saveError && (
          <p className="field_error" role="alert">
            {saveError}
          </p>
        )}

        <button type="submit" className="button button_primary button_wide">
          Save schedule
        </button>
      </form>
    </>
  );
}
