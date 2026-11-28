import { useState } from "react";
import { DogFigure } from "../components/dog_figure.jsx";
import { TextField } from "../components/form_fields.jsx";
import { Mark } from "../components/icons.jsx";
import { signIn } from "../data/store.js";

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function LoginScreen({ onSignedIn }) {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!EMAIL_PATTERN.test(email.trim())) {
      setError("Enter an email address, for example test@example.com.");
      return;
    }
    onSignedIn(await signIn(email));
  };

  return (
    <main className="login">
      <div className="login_art" aria-hidden="true">
        <span className="pedestal" />
        <DogFigure color="butter" mood="happy" className="login_dog login_dog_back" />
        <DogFigure color="blue" mood="excited" className="login_dog login_dog_front" />
        <span className="bubble">Dinner?</span>
      </div>
      <h1 className="wordmark">
        <Mark />
        kibbly
      </h1>
      <p className="login_tagline">Knows every dog. Feeds every dog.</p>
      <form onSubmit={handleSubmit} noValidate className="card login_form">
        <TextField
          label="Email"
          type="email"
          autoComplete="off"
          inputMode="email"
          value={email}
          onChange={setEmail}
          error={error}
        />
        <button type="submit" className="button button_primary button_wide">
          Open preview
        </button>
      </form>
      <p className="login_note">
        This preview has no real accounts, so any test email works. Sign in with a password comes once accounts are
        linked.
      </p>
    </main>
  );
}
