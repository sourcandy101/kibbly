import { useId } from "react";

export function TextField({ label, hint, error, value, onChange, multiline = false, ...inputProps }) {
  const id = useId();
  const messageId = `${id}_message`;
  const shared = {
    id,
    value,
    onChange: (event) => onChange(event.target.value),
    "aria-invalid": error ? true : undefined,
    "aria-describedby": error || hint ? messageId : undefined,
    ...inputProps,
  };
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      {multiline ? <textarea rows={3} {...shared} /> : <input {...shared} />}
      {(error || hint) && (
        <p id={messageId} className={error ? "field_error" : "field_hint"}>
          {error || hint}
        </p>
      )}
    </div>
  );
}

export function ChoiceField({ label, options, error, value, onChange }) {
  const name = useId();
  return (
    <fieldset className="field">
      <legend>{label}</legend>
      <div className="choices">
        {options.map((option) => (
          <label key={option.value} className={value === option.value ? "choice choice_active" : "choice"}>
            <input
              type="radio"
              name={name}
              value={option.value}
              checked={value === option.value}
              onChange={() => onChange(option.value)}
            />
            {option.label}
          </label>
        ))}
      </div>
      {error && <p className="field_error">{error}</p>}
    </fieldset>
  );
}
