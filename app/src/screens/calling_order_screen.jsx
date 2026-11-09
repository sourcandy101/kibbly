import { useState } from "react";
import DogAvatar from "../components/dog_avatar.jsx";
import { saveCallOrder } from "../data/store.js";
import { pathTo } from "../logic/routes.js";

export default function CallingOrderScreen({ data, refresh }) {
  const [announcement, setAnnouncement] = useState("");
  const dogs = data.dogs;

  const move = async (index, offset) => {
    const reordered = [...dogs];
    const [dog] = reordered.splice(index, 1);
    reordered.splice(index + offset, 0, dog);
    await saveCallOrder(reordered.map((entry) => entry.dog_id));
    await refresh();
    setAnnouncement(`${dog.name} is now number ${index + offset + 1}.`);
  };

  return (
    <>
      <header className="page_header">
        <h1>Calling order</h1>
      </header>
      <p className="lead">At each meal time, Kibbly calls your dogs in this order. A shy dog can go first.</p>

      {dogs.length === 0 ? (
        <div className="card empty">
          <p>Add a dog first.</p>
          <a className="button button_primary" href={pathTo("dog_new")}>
            Add a dog
          </a>
        </div>
      ) : (
        <ol className="order_list">
          {dogs.map((dog, index) => (
            <li key={dog.dog_id} className="card order_row">
              <span className="order_rank">{index + 1}</span>
              <DogAvatar name={dog.name} />
              <strong className="order_name">{dog.name}</strong>
              <div className="order_buttons">
                <button
                  type="button"
                  className="icon_button"
                  disabled={index === 0}
                  onClick={() => move(index, -1)}
                  aria-label={`Move ${dog.name} up`}
                >
                  ↑
                </button>
                <button
                  type="button"
                  className="icon_button"
                  disabled={index === dogs.length - 1}
                  onClick={() => move(index, 1)}
                  aria-label={`Move ${dog.name} down`}
                >
                  ↓
                </button>
              </div>
            </li>
          ))}
        </ol>
      )}
      <p className="visually_hidden" aria-live="polite">
        {announcement}
      </p>
    </>
  );
}
