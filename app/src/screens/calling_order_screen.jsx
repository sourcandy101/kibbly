import { useState } from "react";
import DogAvatar from "../components/dog_avatar.jsx";
import { dogColors } from "../components/dog_figure.jsx";
import Icon from "../components/icons.jsx";
import { saveCallOrder } from "../data/store.js";
import { pathTo } from "../logic/routes.js";

export default function CallingOrderScreen({ data, refresh }) {
  const [announcement, setAnnouncement] = useState("");
  const dogs = data.dogs;
  const colors = dogColors(dogs);

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
      <p className="lead">At each meal, Kibbly calls your dogs one by one in this order. Put a shy dog first.</p>

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
              <DogAvatar color={colors[dog.dog_id]} mood={index === 0 ? "excited" : "happy"} />
              <div className="order_name">
                <strong>{dog.name}</strong>
                {index === 0 && <span className="call_bubble">“{dog.name}!”</span>}
              </div>
              <div className="order_buttons">
                <button
                  type="button"
                  className="icon_button"
                  disabled={index === 0}
                  onClick={() => move(index, -1)}
                  aria-label={`Move ${dog.name} up`}
                >
                  <Icon name="up" />
                </button>
                <button
                  type="button"
                  className="icon_button"
                  disabled={index === dogs.length - 1}
                  onClick={() => move(index, 1)}
                  aria-label={`Move ${dog.name} down`}
                >
                  <Icon name="down" />
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
