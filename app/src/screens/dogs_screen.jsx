import { DOG_COLORS, DogFigure, dogColors } from "../components/dog_figure.jsx";
import Icon from "../components/icons.jsx";
import { pathTo } from "../logic/routes.js";
import { ageLabel, localDateIn } from "../logic/time.js";
import { MAX_DOGS } from "../logic/validation.js";

function scheduleSummary(schedule) {
  const count = schedule?.meals.length ?? 0;
  if (count === 0) return "No meal times yet";
  return `${count} ${count === 1 ? "meal" : "meals"}, ${schedule.daily_total_grams} g a day`;
}

export default function DogsScreen({ data }) {
  const today = localDateIn(new Date(), data.home.timezone);
  const isFull = data.dogs.length >= MAX_DOGS;
  const colors = dogColors(data.dogs);

  return (
    <>
      <header className="page_header">
        <h1>Your dogs</h1>
        {!isFull && (
          <a className="button button_primary button_small" href={pathTo("dog_new")}>
            <Icon name="plus" />
            Add a dog
          </a>
        )}
      </header>
      {isFull && <p className="notice">A home can have up to {MAX_DOGS} dogs.</p>}

      {data.dogs.length === 0 ? (
        <div className="card empty">
          <DogFigure color="butter" mood="excited" className="empty_figure" />
          <p>No dogs yet. Add one to set up its meals.</p>
        </div>
      ) : (
        <ul className="dog_list">
          {data.dogs.map((dog) => (
            <li key={dog.dog_id} className="card dog_card">
              <div className="dog_card_art" style={{ background: DOG_COLORS[colors[dog.dog_id]].tint }}>
                <DogFigure color={colors[dog.dog_id]} mood="happy" />
              </div>
              <div className="dog_card_body">
                <h2>{dog.name}</h2>
                <p>
                  {dog.breed}, {ageLabel(dog.birth_month, today)}, {dog.current_weight_kg} kg
                </p>
                <p className="dog_card_meals">
                  <Icon name="clock" />
                  {scheduleSummary(data.schedules[dog.dog_id])}
                </p>
                <div className="button_row">
                  <a className="button button_small" href={pathTo("dog_edit", dog.dog_id)} aria-label={`Edit ${dog.name}'s profile`}>
                    <Icon name="pencil" />
                    Profile
                  </a>
                  <a className="button button_small" href={pathTo("schedule", dog.dog_id)} aria-label={`Edit ${dog.name}'s meal times`}>
                    <Icon name="cal" />
                    Meal times
                  </a>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
