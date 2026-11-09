import { useState } from "react";
import DogAvatar from "../components/dog_avatar.jsx";
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

function MealRow({ row }) {
  const text = STATUS_TEXT[row.status];
  const served = row.grams_dispensed
    ? `Ate ${row.grams_eaten} g of ${row.grams_dispensed} g served`
    : `${row.planned_grams} g planned`;
  return (
    <li className="meal_row">
      <time className="meal_time">{row.local_time}</time>
      <DogAvatar name={row.dog_name} />
      <div className="meal_text">
        <strong>{row.dog_name}</strong>
        <span>
          {row.label}: {text.detail ?? served}
        </span>
      </div>
      <span className={`badge badge_${text.tone}`}>{text.badge}</span>
    </li>
  );
}

const WIFI_TEXT = { online: "Feeder online", offline: "Feeder offline", pairing: "Feeder pairing" };

export default function HomeScreen({ data, refresh, user, onSignOut }) {
  const [confirmingReset, setConfirmingReset] = useState(false);
  const rows = buildTodayMeals(data.dogs, data.schedules, data.meals, data.home.timezone);
  const summary = summarizeToday(rows);
  const { wifi_status: wifiStatus, tank_grams_estimate: tankGrams, tank_capacity_grams: tankCapacity } = data.home.feeder;
  const tankPercent = tankGrams === null ? null : Math.round((tankGrams / tankCapacity) * 100);
  const fedPercent = summary.planned_grams ? Math.min(100, (summary.eaten_grams / summary.planned_grams) * 100) : 0;

  const handleReset = async () => {
    await resetSampleData();
    setConfirmingReset(false);
    await refresh();
  };

  return (
    <>
      <header className="page_header">
        <h1>Today</h1>
        <span className={wifiStatus === "online" ? "status status_on" : "status"}>{WIFI_TEXT[wifiStatus]}</span>
      </header>

      <section className="stats" aria-label="Feeder levels">
        <div className="card stat">
          <h2>Eaten today</h2>
          <p className="stat_value">
            {summary.eaten_grams} <small>of {summary.planned_grams} g</small>
          </p>
          <div className="meter" aria-hidden="true">
            <span style={{ width: `${fedPercent}%` }} />
          </div>
        </div>
        <div className="card stat">
          <h2>Food tank</h2>
          {tankPercent === null ? (
            <p className="stat_value">
              <small>Not known yet</small>
            </p>
          ) : (
            <>
              <p className="stat_value">
                {tankGrams} <small>of {tankCapacity} g</small>
              </p>
              <div className={tankPercent < LOW_TANK_PERCENT ? "meter meter_low" : "meter"} aria-hidden="true">
                <span style={{ width: `${tankPercent}%` }} />
              </div>
            </>
          )}
        </div>
      </section>
      <p className="fine_print">Feeder status, tank level and meal reports are sample values for now.</p>

      <section>
        <h2 className="section_title">Meals</h2>
        {data.dogs.length === 0 ? (
          <div className="card empty">
            <p>No dogs yet. Add your first dog to plan its meals.</p>
            <a className="button button_primary" href={pathTo("dog_new")}>
              Add a dog
            </a>
          </div>
        ) : rows.length === 0 ? (
          <div className="card empty">
            <p>No meals planned yet. Open a dog to set its schedule.</p>
            <a className="button button_primary" href={pathTo("dogs")}>
              Go to dogs
            </a>
          </div>
        ) : (
          <ul className="card meal_list">
            {rows.map((row) => (
              <MealRow key={row.key} row={row} />
            ))}
          </ul>
        )}
      </section>

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
            <button type="button" className="button" onClick={() => setConfirmingReset(true)}>
              Reset sample data
            </button>
            <button type="button" className="button" onClick={onSignOut}>
              Sign out
            </button>
          </div>
        )}
      </footer>
    </>
  );
}
