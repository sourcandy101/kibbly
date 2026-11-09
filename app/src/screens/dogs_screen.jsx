import DogAvatar from "../components/dog_avatar.jsx";
import { pathTo } from "../logic/routes.js";
import { ageLabel, localDateIn } from "../logic/time.js";
import { MAX_DOGS } from "../logic/validation.js";

function scheduleSummary(schedule) {
  const count = schedule?.meals.length ?? 0;
  if (count === 0) return "No schedule yet";
  return `${count} ${count === 1 ? "meal" : "meals"}, ${schedule.daily_total_grams} g a day`;
}

export default function DogsScreen({ data }) {
  const today = localDateIn(new Date(), data.home.timezone);
  const isFull = data.dogs.length >= MAX_DOGS;

  return (
    <>
      <header className="page_header">
        <h1>Dogs</h1>
        {!isFull && (
          <a className="button button_primary" href={pathTo("dog_new")}>
            Add a dog
          </a>
        )}
      </header>
      {isFull && <p className="notice">A home can have up to {MAX_DOGS} dogs.</p>}

      {data.dogs.length === 0 ? (
        <div className="card empty">
          <p>No dogs yet. Add one to set up its meals.</p>
        </div>
      ) : (
        <ul className="dog_list">
          {data.dogs.map((dog) => (
            <li key={dog.dog_id} className="card dog_card">
              <div className="dog_card_top">
                <DogAvatar name={dog.name} />
                <div className="meal_text">
                  <strong>{dog.name}</strong>
                  <span>
                    {dog.breed}, {ageLabel(dog.birth_month, today)}, {dog.current_weight_kg} kg
                  </span>
                  <span>{scheduleSummary(data.schedules[dog.dog_id])}</span>
                </div>
              </div>
              <div className="button_row">
                <a className="button" href={pathTo("dog_edit", dog.dog_id)} aria-label={`Edit ${dog.name}'s profile`}>
                  Profile
                </a>
                <a className="button" href={pathTo("schedule", dog.dog_id)} aria-label={`Edit ${dog.name}'s schedule`}>
                  Schedule
                </a>
              </div>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
