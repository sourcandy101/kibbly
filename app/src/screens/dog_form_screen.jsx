import { useState } from "react";
import { ChoiceField, TextField } from "../components/form_fields.jsx";
import { deleteDog, saveDog } from "../data/store.js";
import { go, pathTo } from "../logic/routes.js";
import { localDateIn } from "../logic/time.js";
import { ACTIVITY_LEVELS, BODY_CONDITIONS, SEX_OPTIONS, validateDog } from "../logic/validation.js";

const capitalize = (text) => text.charAt(0).toUpperCase() + text.slice(1);
const toOptions = (values) => values.map((value) => ({ value, label: capitalize(value) }));
const YES_NO = toOptions(["yes", "no"]);

function emptyForm(today) {
  return {
    name: "",
    breed: "",
    sex: "",
    neutered: "",
    birth_month: "",
    activity: "medium",
    body_condition: "",
    current_weight_kg: "",
    weight_measured_on: today,
    notes: "",
  };
}

function toForm(dog) {
  return {
    name: dog.name,
    breed: dog.breed,
    sex: dog.sex,
    neutered: dog.neutered ? "yes" : "no",
    birth_month: dog.birth_month,
    activity: dog.activity,
    body_condition: dog.body_condition,
    current_weight_kg: String(dog.current_weight_kg),
    weight_measured_on: dog.weight_measured_on,
    notes: dog.notes ?? "",
  };
}

export default function DogFormScreen({ data, refresh, dogId = null }) {
  const today = localDateIn(new Date(), data.home.timezone);
  const dog = dogId ? data.dogs.find((entry) => entry.dog_id === dogId) : null;
  const [form, setForm] = useState(() => (dog ? toForm(dog) : emptyForm(today)));
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
    const result = validateDog(form, today);
    setErrors(result.errors);
    setSaveError("");
    if (!result.ok) {
      // Bring the first problem into view on a small screen.
      requestAnimationFrame(() => document.querySelector(".field_error")?.scrollIntoView({ block: "center" }));
      return;
    }
    try {
      const saved = await saveDog(result.value, dogId);
      await refresh();
      go("schedule", saved.dog_id);
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
        <ChoiceField
          label="Neutered"
          options={YES_NO}
          value={form.neutered}
          onChange={setField("neutered")}
          error={errors.neutered}
        />
        <TextField
          label="Birth month"
          type="month"
          max={today.slice(0, 7)}
          hint="An estimate is fine. Kibbly works out the age from this."
          value={form.birth_month}
          onChange={setField("birth_month")}
          error={errors.birth_month}
        />
        <ChoiceField
          label="Activity"
          options={toOptions(ACTIVITY_LEVELS)}
          value={form.activity}
          onChange={setField("activity")}
          error={errors.activity}
        />
        <ChoiceField
          label="Body condition"
          options={toOptions(BODY_CONDITIONS)}
          value={form.body_condition}
          onChange={setField("body_condition")}
          error={errors.body_condition}
        />
        <div className="field_pair">
          <TextField
            label="Weight in kg"
            inputMode="decimal"
            value={form.current_weight_kg}
            onChange={setField("current_weight_kg")}
            error={errors.current_weight_kg}
            autoComplete="off"
          />
          <TextField
            label="Weighed on"
            type="date"
            max={today}
            value={form.weight_measured_on}
            onChange={setField("weight_measured_on")}
            error={errors.weight_measured_on}
          />
        </div>
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
              <p>Remove {dog.name} with its schedule, weights and meal history? This cannot be undone.</p>
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
