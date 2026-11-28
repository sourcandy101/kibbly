import { useEffect, useRef, useState } from "react";
import { dogColors } from "../components/dog_figure.jsx";
import DogAvatar from "../components/dog_avatar.jsx";
import Icon, { Mark } from "../components/icons.jsx";
import { DEFAULT_SERVER, getServerUrl, setServerUrl, streamKibbly } from "../data/ai.js";
import { pathTo } from "../logic/routes.js";
import { buildTodayMeals } from "../logic/today_meals.js";

function ageMonths(birthMonth) {
  if (!birthMonth) return null;
  const [year, month] = birthMonth.split("-").map(Number);
  const now = new Date();
  return Math.max(0, (now.getFullYear() - year) * 12 + (now.getMonth() + 1 - month));
}

function dogPayload(dog) {
  return {
    name: dog.name,
    breed: dog.breed,
    sex: dog.sex,
    neutered: dog.neutered,
    activity: dog.activity,
    body_condition: dog.body_condition,
    weight_kg: dog.current_weight_kg,
    age_months: ageMonths(dog.birth_month),
  };
}

// Plain log lines for the model to ground on: today's meals for this dog.
function factsFor(dog, data) {
  const rows = buildTodayMeals(data.dogs, data.schedules, data.meals, data.home.timezone).filter(
    (row) => row.dog_id === dog.dog_id,
  );
  const facts = rows.map((row) => {
    if (row.grams_dispensed != null) {
      return `${row.local_time} ${row.label}: ${row.status}, ate ${row.grams_eaten} of ${row.grams_dispensed} g.`;
    }
    return `${row.local_time} ${row.label}: ${row.status}, ${row.planned_grams} g planned.`;
  });
  facts.push(`${dog.name} weighs ${dog.current_weight_kg} kg.`);
  return facts;
}

const SUGGESTIONS = (name) => [
  `How did ${name} eat today?`,
  `Is ${name} eating normally?`,
  `What should I watch for?`,
];

function Bubble({ message, color }) {
  const mine = message.role === "you";
  const dots = !mine && message.pending && !message.text;
  return (
    <li className={mine ? "bubble_row mine" : "bubble_row"}>
      {!mine &&
        (message.error ? (
          <span className="kibbly_mark warn">
            <Icon name="alert" />
          </span>
        ) : (
          <span className="kibbly_mark">
            <Mark />
          </span>
        ))}
      <div className={`bubble_msg ${mine ? "mine" : message.error ? "error" : ""} ${dots ? "typing" : ""}`}>
        {dots ? (
          <>
            <i></i>
            <i></i>
            <i></i>
          </>
        ) : (
          message.text
        )}
      </div>
      {mine && color && <DogAvatar color={color} mood="happy" size="small" />}
    </li>
  );
}

export default function ChatScreen({ data }) {
  const dogs = data.dogs;
  const colors = dogColors(dogs);
  const [dogId, setDogId] = useState(dogs[0]?.dog_id);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [pending, setPending] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [server, setServer] = useState(getServerUrl());
  const listEnd = useRef(null);

  const dog = dogs.find((entry) => entry.dog_id === dogId) ?? dogs[0];

  // A fresh welcome whenever the chosen dog changes.
  useEffect(() => {
    if (dog) setMessages([{ role: "kibbly", text: `Hi! Ask me anything about ${dog.name}'s meals.` }]);
  }, [dogId]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    listEnd.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, pending]);

  if (dogs.length === 0) {
    return (
      <>
        <header className="page_header">
          <h1>Ask Kibbly</h1>
        </header>
        <div className="card empty">
          <p>Add a dog first, then Kibbly can answer about its meals.</p>
          <a className="button button_primary" href={pathTo("dog_new")}>
            Add a dog
          </a>
        </div>
      </>
    );
  }

  // Replace the last message (the Kibbly bubble being streamed into).
  const setLast = (patch) =>
    setMessages((current) => {
      const copy = [...current];
      copy[copy.length - 1] = { ...copy[copy.length - 1], ...patch };
      return copy;
    });

  const send = async (text) => {
    const question = (text ?? input).trim();
    if (!question || pending) return;
    setInput("");
    setMessages((current) => [
      ...current,
      { role: "you", text: question },
      { role: "kibbly", text: "", pending: true },
    ]);
    setPending(true);
    try {
      let answer = "";
      await streamKibbly({ dog: dogPayload(dog), question, facts: factsFor(dog, data) }, (piece) => {
        answer += piece;
        setLast({ text: answer, pending: false });
      });
      if (!answer.trim()) setLast({ text: "I don't have an answer for that yet.", pending: false });
    } catch {
      setShowSettings(true);
      setLast({
        error: true,
        pending: false,
        text: `I couldn't reach the Kibbly server at ${getServerUrl()}. On your laptop, start it with "uvicorn kibbly_ai.api.app:app --host 0.0.0.0 --port 8000" and make sure Ollama is running, then set the address below.`,
      });
    } finally {
      setPending(false);
    }
  };

  const saveServer = () => {
    setServerUrl(server.trim() || DEFAULT_SERVER);
    setServer(getServerUrl());
    setShowSettings(false);
  };

  return (
    <div className="chat">
      <header className="page_header">
        <h1>Ask Kibbly</h1>
        <button
          type="button"
          className="icon_button"
          aria-label="Server settings"
          aria-pressed={showSettings}
          onClick={() => setShowSettings((open) => !open)}
        >
          <Icon name="pencil" />
        </button>
      </header>

      {dogs.length > 1 && (
        <div className="ph-dogs chat_dogs" role="group" aria-label="Choose a dog">
          {dogs.map((entry) => (
            <button
              key={entry.dog_id}
              type="button"
              className={entry.dog_id === dogId ? "pill on" : "pill"}
              onClick={() => setDogId(entry.dog_id)}
            >
              <span className="av">
                <DogAvatar color={colors[entry.dog_id]} mood="happy" size="small" />
              </span>
              {entry.name}
            </button>
          ))}
        </div>
      )}

      {showSettings && (
        <div className="card server_box">
          <label htmlFor="server">Kibbly server address</label>
          <input id="server" value={server} onChange={(event) => setServer(event.target.value)} inputMode="url" />
          <p className="field_hint">
            The AI server on your laptop, on the same network. Chat and recognition run there.
          </p>
          <button type="button" className="button button_small" onClick={saveServer}>
            Save address
          </button>
        </div>
      )}

      <ul className="chat_list">
        {messages.map((message, index) => (
          <Bubble key={index} message={message} color={colors[dogId]} />
        ))}
        <li ref={listEnd} />
      </ul>

      {messages.length <= 1 && (
        <div className="suggestions">
          {SUGGESTIONS(dog.name).map((text) => (
            <button key={text} type="button" className="chip" onClick={() => send(text)}>
              {text}
            </button>
          ))}
        </div>
      )}

      <form
        className="composer"
        onSubmit={(event) => {
          event.preventDefault();
          send();
        }}
      >
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder={`Ask about ${dog.name}...`}
          aria-label={`Ask about ${dog.name}`}
          autoComplete="off"
        />
        <button type="submit" className="send" disabled={pending || !input.trim()} aria-label="Send">
          <Icon name="send" />
        </button>
      </form>
      <p className="fine_print">Kibbly answers from this dog's logs only, and never gives medical advice.</p>
    </div>
  );
}
