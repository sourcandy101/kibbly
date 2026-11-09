// Combines schedules and meal logs into the list shown on the home screen.

function isSameLocalDay(isoTime, now) {
  const date = new Date(isoTime);
  return (
    date.getFullYear() === now.getFullYear() &&
    date.getMonth() === now.getMonth() &&
    date.getDate() === now.getDate()
  );
}

export function clockTime(date) {
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${hours}:${minutes}`;
}

// Status of each row:
//   done       the feeder logged this meal today
//   upcoming   the meal time has not arrived
//   no_report  the meal time passed with no log from the feeder
export function buildTodayMeals(dogs, schedules, mealLogs, now = new Date()) {
  const currentTime = clockTime(now);
  const orderedDogs = [...dogs].sort((a, b) => a.call_order - b.call_order);
  const todayLogs = mealLogs.filter((log) => isSameLocalDay(log.time, now));

  const rows = orderedDogs.flatMap((dog) => {
    const planned = schedules[dog.id]?.meals ?? [];
    return planned.map((meal) => {
      const log = todayLogs.find((entry) => entry.dog_id === dog.id && entry.scheduled_time === meal.time);
      let status = "no_report";
      if (log) status = "done";
      else if (meal.time > currentTime) status = "upcoming";
      return {
        key: `${dog.id}_${meal.time}`,
        dog_id: dog.id,
        dog_name: dog.name,
        call_order: dog.call_order,
        time: meal.time,
        planned_grams: meal.grams,
        grams_served: log?.grams_served ?? null,
        grams_eaten: log?.grams_eaten ?? null,
        status,
      };
    });
  });

  return rows.sort((a, b) => a.time.localeCompare(b.time) || a.call_order - b.call_order);
}

export function summarizeToday(rows) {
  return {
    planned_grams: rows.reduce((sum, row) => sum + row.planned_grams, 0),
    eaten_grams: rows.reduce((sum, row) => sum + (row.grams_eaten ?? 0), 0),
  };
}
