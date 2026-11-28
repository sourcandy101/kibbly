import { useState } from "react";
import DogAvatar from "../components/dog_avatar.jsx";
import { DOG_COLORS, DogFigure, dogColors } from "../components/dog_figure.jsx";
import Icon, { Mark } from "../components/icons.jsx";
import { resetSampleData } from "../data/store.js";
import { pathTo } from "../logic/routes.js";
import { buildTodayMeals, summarizeToday } from "../logic/today_meals.js";

const LOW_TANK_PERCENT = 20;

// Text for each meal status in schemas/meal.json, plus upcoming and no_report.
const STATUS_TEXT = {
  completed: { badge: "Done", tone: "good" },
  partial: { badge: "Partial", tone: "warn" },
  served_offline: { badge: "Offline", tone: "warn" },
  missed_no_show: { badge: "Skipped", tone: "warn", detail: "Did not come" },
  not_served_empty_tank: { badge: "Not served", tone: "bad", detail: "The tank was empty" },
  not_served_jam: { badge: "Not served", tone: "bad", detail: "The feeder was jammed" },
  not_served_power_cut: { badge: "Not served", tone: "bad", detail: "There was a power cut" },
  upcoming: { badge: "Upcoming", tone: "quiet" },
  no_report: { badge: "No report", tone: "warn" },
};

const moodFor = (tone) => (tone === "good" || tone === "quiet" ? "happy" : "sad");

function greeting(email, now) {
  const hour = now.getHours();
  const part = hour < 12 ? "morning" : hour < 18 ? "afternoon" : "evening";
  const day = now.toLocaleDateString("en-GB", { weekday: "long" });
  const first = email.split(/[@._+\d-]/)[0] || "there";
  return { when: `${day} ${part}`, name: first.charAt(0).toUpperCase() + first.slice(1) };
}

function DogTile({ dog, color, rows }) {
  const { planned_grams: planned, eaten_grams: eaten } = summarizeToday(rows);
  const sad = rows.some((row) => moodFor(STATUS_TEXT[row.status]?.tone) === "sad");
  const percent = planned ? Math.min(100, (eaten / planned) * 100) : 0;
  return (
    <li className="dog_tile" style={{ background: DOG_COLORS[color].tint }}>
      <DogFigure color={color} mood={sad ? "sad" : eaten > 0 ? "eating" : "happy"} className="dog_tile_figure" />
      <strong>{dog.name}</strong>
      <p className="dog_tile_grams">
        <span className="number">{eaten}</span> of {planned} g
      </p>
      <div className="meter" aria-hidden="true">
        <span style={{ width: `${percent}%` }} />
      </div>
    </li>
  );
}

function MealRow({ row, color }) {
  const text = STATUS_TEXT[row.status];
  const served = row.grams_dispensed
    ? `ate ${row.grams_eaten} of ${row.grams_dispensed} g`
    : `${row.planned_grams} g planned`;
  return (
    <li className="meal_row">
      <time className="meal_time">{row.local_time}</time>
      <DogAvatar color={color} mood={moodFor(text.tone)} size="small" />
      <div className="meal_text">
        <strong>{row.dog_name}</strong>
        <span>
          {row.label}, {text.detail ? text.detail.toLowerCase() : served}
        </span>
      </div>
      <span className={`badge badge_${text.tone}`}>{text.badge}</span>
    </li>
  );
}

const WIFI_TEXT = { online: "Feeder online", offline: "Feeder offline", pairing: "Pairing" };

export default function HomeScreen({ data, refresh, user, onSignOut }) {
  const [confirmingReset, setConfirmingReset] = useState(false);
  const rows = buildTodayMeals(data.dogs, data.schedules, data.meals, data.home.timezone);
  const colors = dogColors(data.dogs);
  const hello = greeting(user.email, new Date());
  const { wifi_status: wifiStatus, tank_grams_estimate: tankGrams, tank_capacity_grams: tankCapacity } = data.home.feeder;
  const tankPercent = tankGrams === null ? null : Math.round((tankGrams / tankCapacity) * 100);
  const tankLow = tankPercent !== null && tankPercent < LOW_TANK_PERCENT;

  const handleReset = async () => {
    await resetSampleData();
    setConfirmingReset(false);
    await refresh();
  };

  return (
    <>
      <header className="top_bar">
        <span className="brand">
          <Mark />
          kibbly
        </span>
        <span className={`status status_${wifiStatus}`}>
          <Icon name="wifi" />
          {WIFI_TEXT[wifiStatus]}
        </span>
      </header>

      <div className="hello">
        <p>{hello.when}</p>
        <h1>Hi {hello.name}</h1>
      </div>

      {data.dogs.length === 0 ? (
        <div className="card empty">
          <DogFigure color="butter" mood="excited" className="empty_figure" />
          <p>Add your first dog and Kibbly will plan its meals.</p>
          <a className="button button_primary" href={pathTo("dog_new")}>
            Add a dog
          </a>
        </div>
      ) : (
        <>
          <ul className="dog_tiles" aria-label="Eaten today">
            {data.dogs.map((dog) => (
              <DogTile key={dog.dog_id} dog={dog} color={colors[dog.dog_id]} rows={rows.filter((row) => row.dog_id === dog.dog_id)} />
            ))}
          </ul>

          <section className="card tank" aria-label="Food tank">
            <div className="tank_text">
              <h2>Food tank</h2>
              {tankPercent === null ? (
                <p>Not measured yet</p>
              ) : (
                <p>
                  <span className="number">{tankGrams}</span> of {tankCapacity} g
                  {tankLow && <span className="tank_low">Refill soon</span>}
                </p>
              )}
            </div>
            {tankPercent !== null && (
              <div className={tankLow ? "kibble_meter kibble_meter_low" : "kibble_meter"} aria-hidden="true">
                <span style={{ width: `${tankPercent}%` }} />
              </div>
            )}
          </section>

          <section>
            <h2 className="section_title">Today's meals</h2>
            {rows.length === 0 ? (
              <div className="card empty">
                <p>No meals planned yet. Open a dog to set its meal times.</p>
                <a className="button button_primary" href={pathTo("dogs")}>
                  Go to dogs
                </a>
              </div>
            ) : (
              <ul className="card meal_list">
                {rows.map((row) => (
                  <MealRow key={row.key} row={row} color={colors[row.dog_id]} />
                ))}
              </ul>
            )}
          </section>
        </>
      )}
      <p className="fine_print">Feeder status, tank level and meal reports are sample values for now.</p>

      <footer className="page_footer">
        <p>Signed in as {user.email}</p>
        {confirmingReset ? (
          <div className="confirm" role="group" aria-label="Confirm reset">
            <p>Replace everything in this preview with the sample dogs?</p>
            <div className="button_row">
              <button type="button" className="button button_danger" onClick={handleReset}>
                Reset
              </button>
              <button type="button" className="button" onClick={() => setConfirmingReset(false)}>
                Keep my data
              </button>
            </div>
          </div>
        ) : (
          <div className="button_row">
            <button type="button" className="link_button" onClick={() => setConfirmingReset(true)}>
              Reset sample data
            </button>
            <button type="button" className="link_button" onClick={onSignOut}>
              Sign out
            </button>
          </div>
        )}
      </footer>
    </>
  );
}
