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

const DEFAULT_MEAL_COUNT = 2;

function initialRows(schedule) {
  const saved = schedule?.meals ?? [];
  if (saved.length > 0) return saved.map((meal) => ({ local_time: meal.local_time, grams: String(meal.grams) }));
  return defaultTimes(DEFAULT_MEAL_COUNT).map((local_time) => ({ local_time, grams: "" }));
}

function stepGrams(current, direction) {
  const value = parseNumber(current) ?? 0;
  const stepped =
    direction > 0
      ? Math.floor(value / GRAM_STEP) * GRAM_STEP + GRAM_STEP
      : Math.ceil(value / GRAM_STEP) * GRAM_STEP - GRAM_STEP;
  return String(Math.min(MAX_GRAMS_PER_MEAL, Math.max(GRAM_STEP, stepped)));
}

export default function ScheduleScreen({ data, refresh, dogId }) {
  const dog = data.dogs.find((entry) => entry.dog_id === dogId);
  const schedule = data.schedules[dogId];
  const nextRowId = useRef(0);
  const withId = (row) => ({ ...row, id: nextRowId.current++ });

  const [rows, setRows] = useState(() => (dog ? initialRows(schedule).map(withId) : []));
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
    setRows((current) => [...current, withId({ local_time: nextFreeTime(current.map((row) => row.local_time)), grams: "" })]);
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

  return (
    <>
      <header className="page_header">
        <h1>{dog.name}'s meals</h1>
        <a className="button" href={pathTo("dogs")}>
          Cancel
        </a>
      </header>

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
                      value={row.local_time}
                      onChange={(event) => updateRow(row.id, "local_time", event.target.value)}
                      aria-invalid={errors.local_time ? true : undefined}
                    />
                    {errors.local_time && <p className="field_error">{errors.local_time}</p>}
                  </div>
                  <div className="field">
                    <label htmlFor={`grams_${row.id}`}>Grams</label>
                    <div className="stepper">
                      <button
                        type="button"
                        onClick={() => updateRow(row.id, "grams", stepGrams(row.grams, -1))}
                        aria-label={`${GRAM_STEP} g less for meal ${index + 1}`}
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
                        aria-label={`${GRAM_STEP} g more for meal ${index + 1}`}
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
