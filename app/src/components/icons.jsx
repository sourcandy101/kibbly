// Line icons from the pitch deck, so the app and the slides share one drawing style.

const PATHS = {
  bowl: (
    <>
      <path d="M3.5 11h17l-1.6 6.4A3 3 0 0 1 16 20H8a3 3 0 0 1-2.9-2.6z" />
      <path d="M8 11a4 4 0 0 1 8 0" />
    </>
  ),
  dogs: (
    <>
      <circle cx="8" cy="9" r="3.2" />
      <circle cx="16.5" cy="10.5" r="2.6" />
      <path d="M2.5 19a5.5 5.5 0 0 1 11 0M12.5 19a4.2 4.2 0 0 1 8.5 0" />
    </>
  ),
  speaker: (
    <>
      <path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" />
      <path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11" />
    </>
  ),
  clock: (
    <>
      <circle cx="12" cy="12" r="9" />
      <path d="M12 7v5l3 2" />
    </>
  ),
  check: <path d="M5 12.5l4.5 4.5L19 7.5" />,
  x: <path d="M7 7l10 10M17 7 7 17" />,
  plus: <path d="M12 5v14M5 12h14" />,
  minus: <path d="M5 12h14" />,
  up: <path d="M12 19V5M6 11l6-6 6 6" />,
  down: <path d="M12 5v14M6 13l6 6 6-6" />,
  alert: (
    <>
      <path d="M12 4 21 19.5H3z" />
      <path d="M12 10v4.5M12 17.2v.1" />
    </>
  ),
  wifi: (
    <>
      <path d="M3 9.5a13 13 0 0 1 18 0M6 13a8.5 8.5 0 0 1 12 0M9 16.5a4 4 0 0 1 6 0" />
      <path d="M12 20v.1" />
    </>
  ),
  cal: (
    <>
      <rect x="4" y="5" width="16" height="15" rx="2.5" />
      <path d="M4 10h16M9 3v4M15 3v4" />
    </>
  ),
  pencil: <path d="M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4" />,
  paw: (
    <g fill="currentColor" stroke="none">
      <ellipse cx="12" cy="15.6" rx="4.8" ry="3.9" />
      <circle cx="5.8" cy="10.6" r="2.1" />
      <circle cx="9.4" cy="6.6" r="2.1" />
      <circle cx="14.6" cy="6.6" r="2.1" />
      <circle cx="18.2" cy="10.6" r="2.1" />
    </g>
  ),
};

export default function Icon({ name, className = "icon" }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2.1"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      className={className}
    >
      {PATHS[name]}
    </svg>
  );
}

// The Kibbly logo: a heart over a bowl, from the pitch deck.
export function Mark({ className = "mark" }) {
  return (
    <svg viewBox="0 0 100 100" aria-hidden="true" className={className}>
      <rect width="100" height="100" rx="30" fill="#2E1433" />
      <path d="M50 47c-10-6-17-12-13-20 3-5 10-5 13 1 3-6 10-6 13-1 4 8-3 14-13 20z" fill="#FF5C9A" />
      <path d="M20 54h60c-3 17-15 25-30 25S23 71 20 54z" fill="#FFF9FB" />
      <path d="M27 62c8 4 38 4 46 0" stroke="#C9A15E" strokeWidth="3" fill="none" strokeLinecap="round" />
    </svg>
  );
}
