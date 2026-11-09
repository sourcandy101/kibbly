import { useState } from "react";
import { ChoiceField, TextField } from "../components/form_fields.jsx";
import { deleteDog, saveDog } from "../data/store.js";
import { go, pathTo } from "../logic/routes.js";
import { ACTIVITY_LEVELS, MAX_MEALS_PER_DAY, SEX_OPTIONS, validateDog } from "../logic/validation.js";

const capitalize = (text) => text.charAt(0).toUpperCase() + text.slice(1);
const toOptions = (values) => values.map((value) => ({ value, label: capitalize(String(value)) }));
const MEAL_COUNTS = Array.from({ length: MAX_MEALS_PER_DAY }, (_, index) => String(index + 1));

const EMPTY_FORM = {
  name: "",
  breed: "",
  sex: "",
  age_months: "",
  weight_kg: "",
  activity: "medium",
  meals_per_day: "2",
  notes: "",
};

function toForm(dog) {
  return {
    ...EMPTY_FORM,
    ...dog,
    age_months: String(dog.age_months),
    weight_kg: String(dog.weight_kg),
    meals_per_day: String(dog.meals_per_day),
  };
}

export default function DogFormScreen({ data, refresh, dogId = null }) {
  const dog = dogId ? data.dogs.find((entry) => entry.id === dogId) : null;
  const [form, setForm] = useState(() => (dog ? toForm(dog) : EMPTY_FORM));
  const [errors, setErrors] = useState({});
  const [saveError, setSaveError] = useState("");
  const [confirmingDelete, setConfirmingDelete] = useState(false);

  if (dogId && !dog) {
    return (
      <div className="card empty">
        <p>This dog no longer exists.</p>
        <a className="button" href={pathTo("dogs")}>
          Back to dogs
        </a>
      </div>
    );
  }

  const setField = (field) => (value) => {
    setForm((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: undefined }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const result = validateDog(form);
    setErrors(result.errors);
    setSaveError("");
    if (!result.ok) {
      // Bring the first problem into view on a small screen.
      requestAnimationFrame(() => document.querySelector("[aria-invalid='true'], .field_error")?.scrollIntoView({ block: "center" }));
      return;
    }
    try {
      const saved = await saveDog(result.value, dogId);
      await refresh();
      go("schedule", saved.id);
    } catch (error) {
      setSaveError(error.message);
    }
  };

  const handleDelete = async () => {
    await deleteDog(dogId);
    await refresh();
    go("dogs");
  };

  return (
    <>
      <header className="page_header">
        <h1>{dog ? `Edit ${dog.name}` : "New dog"}</h1>
        <a className="button" href={pathTo("dogs")}>
          Cancel
        </a>
      </header>

      <form onSubmit={handleSubmit} noValidate className="card form">
        <TextField label="Name" value={form.name} onChange={setField("name")} error={errors.name} autoComplete="off" />
        <TextField label="Breed" value={form.breed} onChange={setField("breed")} error={errors.breed} autoComplete="off" />
        <ChoiceField
          label="Sex"
          options={toOptions(SEX_OPTIONS)}
          value={form.sex}
          onChange={setField("sex")}
          error={errors.sex}
        />
        <div className="field_pair">
          <TextField
            label="Age in months"
            inputMode="numeric"
            value={form.age_months}
            onChange={setField("age_months")}
            error={errors.age_months}
            autoComplete="off"
          />
          <TextField
            label="Weight in kg"
            inputMode="decimal"
            value={form.weight_kg}
            onChange={setField("weight_kg")}
            error={errors.weight_kg}
            autoComplete="off"
          />
        </div>
        <ChoiceField
          label="Activity"
          options={toOptions(ACTIVITY_LEVELS)}
          value={form.activity}
          onChange={setField("activity")}
          error={errors.activity}
        />
        <ChoiceField
          label="Meals per day"
          options={toOptions(MEAL_COUNTS)}
          value={form.meals_per_day}
          onChange={setField("meals_per_day")}
          error={errors.meals_per_day}
        />
        <TextField
          label="Notes (optional)"
          multiline
          value={form.notes}
          onChange={setField("notes")}
          error={errors.notes}
        />
        <div className="field">
          <p className="field_label">Photos and video</p>
          <p className="placeholder_box">Uploads open once Firebase is linked. Recognition will use them.</p>
        </div>
        {saveError && (
          <p className="field_error" role="alert">
            {saveError}
          </p>
        )}
        <button type="submit" className="button button_primary button_wide">
          Save and set schedule
        </button>
      </form>

      {dog && (
        <section className="danger_zone">
          {confirmingDelete ? (
            <div className="confirm" role="group" aria-label="Confirm removal">
              <p>Remove {dog.name} with its schedule and meal history? This cannot be undone.</p>
              <div className="button_row">
                <button type="button" className="button button_danger" onClick={handleDelete}>
                  Remove {dog.name}
                </button>
                <button type="button" className="button" onClick={() => setConfirmingDelete(false)}>
                  Keep
                </button>
              </div>
            </div>
          ) : (
            <button type="button" className="button" onClick={() => setConfirmingDelete(true)}>
              Remove this dog
            </button>
          )}
        </section>
      )}
    </>
  );
}
