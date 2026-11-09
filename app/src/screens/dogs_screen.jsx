import DogAvatar from "../components/dog_avatar.jsx";
import { pathTo } from "../logic/routes.js";

function scheduleSummary(schedule) {
  const meals = schedule?.meals ?? [];
  if (meals.length === 0) return "No schedule yet";
  const total = meals.reduce((sum, meal) => sum + meal.grams, 0);
  return `${meals.length} ${meals.length === 1 ? "meal" : "meals"}, ${total} g a day`;
}

export default function DogsScreen({ data }) {
  return (
    <>
      <header className="page_header">
        <h1>Dogs</h1>
        <a className="button button_primary" href={pathTo("dog_new")}>
          Add a dog
        </a>
      </header>

      {data.dogs.length === 0 ? (
        <div className="card empty">
          <p>No dogs yet. Add one to set up its meals.</p>
        </div>
      ) : (
        <ul className="dog_list">
          {data.dogs.map((dog) => (
            <li key={dog.id} className="card dog_card">
              <div className="dog_card_top">
                <DogAvatar name={dog.name} />
                <div className="meal_text">
                  <strong>{dog.name}</strong>
                  <span>
                    {dog.breed}, {dog.age_months} months, {dog.weight_kg} kg
                  </span>
                  <span>{scheduleSummary(data.schedules[dog.id])}</span>
                </div>
              </div>
              <div className="button_row">
                <a className="button" href={pathTo("dog_edit", dog.id)} aria-label={`Edit ${dog.name}'s profile`}>
                  Profile
                </a>
                <a className="button" href={pathTo("schedule", dog.id)} aria-label={`Edit ${dog.name}'s schedule`}>
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
