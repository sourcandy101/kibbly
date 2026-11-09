import { useState } from "react";
import { TextField } from "../components/form_fields.jsx";
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
      <img src="/icon.svg" alt="" className="login_logo" />
      <h1>Kibbly</h1>
      <p className="login_tagline">Knows every dog. Feeds every dog.</p>
      <form onSubmit={handleSubmit} noValidate className="card">
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
        This is a preview without real accounts. Use any test email. Real sign in with a password arrives when Firebase
        is linked.
      </p>
    </main>
  );
}
