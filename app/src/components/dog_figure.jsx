// The Kibbly dog character from the pitch deck, drawn in the dog's own color.
// mood: "happy", "sad", "eating" or "excited".

const INK = "#2E1433";

export const DOG_COLORS = {
  butter: { body: "#FFD66B", ear: "#EFAE3C", tint: "#FFF3C9" },
  blue: { body: "#8AABF7", ear: "#5D84E3", tint: "#DCE6FF" },
  pink: { body: "#FFA2C6", ear: "#F27AA8", tint: "#FFE1EC" },
  mint: { body: "#90DEBF", ear: "#5EC49C", tint: "#DDF7EB" },
  lilac: { body: "#BEA7F6", ear: "#9A7FE6", tint: "#EFE8FF" },
};

const PALETTE = ["butter", "blue", "pink", "mint", "lilac"];

function hashColor(dogId) {
  let hash = 7;
  for (const letter of dogId) hash = (hash * 33 + letter.charCodeAt(0)) % 1009;
  return hash % PALETTE.length;
}

// One color per dog: the same on every screen and every phone, and never shared by two dogs of a home.
export function dogColors(dogs) {
  const colors = {};
  const taken = new Set();
  for (const dog of [...dogs].sort((a, b) => a.dog_id.localeCompare(b.dog_id))) {
    let index = hashColor(dog.dog_id);
    while (taken.has(PALETTE[index]) && taken.size < PALETTE.length) index = (index + 1) % PALETTE.length;
    taken.add(PALETTE[index]);
    colors[dog.dog_id] = PALETTE[index];
  }
  return colors;
}

const line = { stroke: INK, strokeWidth: 3.5, strokeLinecap: "round", strokeLinejoin: "round", fill: "none" };

function Face({ mood }) {
  if (mood === "sad") {
    return (
      <>
        <path d="M72 83 L87 77 M128 83 L113 77" {...line} />
        <circle cx="83" cy="91" r="5" fill={INK} />
        <circle cx="117" cy="91" r="5" fill={INK} />
        <circle cx="84.6" cy="89.4" r="1.6" fill="#fff" />
        <circle cx="118.6" cy="89.4" r="1.6" fill="#fff" />
        <path d="M92 98 q8 -4 16 0 q-2 8 -8 9 q-6 -1 -8 -9z" fill={INK} />
        <path d="M100 107 v3 M90 117 q10 -8 20 0" {...line} />
      </>
    );
  }
  if (mood === "excited") {
    return (
      <>
        <path d="M75 90 q7 -9 14 0 M111 90 q7 -9 14 0" {...line} />
        <path d="M92 98 q8 -4 16 0 q-2 8 -8 9 q-6 -1 -8 -9z" fill={INK} />
        <path d="M100 106 v3" {...line} />
        <path d="M87 110 q13 18 26 0 z" fill={INK} />
        <path d="M94 116 q6 10 12 0 z" fill="#FF7BAA" />
      </>
    );
  }
  const eyes =
    mood === "eating" ? (
      <path d="M75 88 q7 6 14 0 M111 88 q7 6 14 0" {...line} />
    ) : (
      <>
        <circle cx="83" cy="87" r="5.6" fill={INK} />
        <circle cx="117" cy="87" r="5.6" fill={INK} />
        <circle cx="84.8" cy="85.2" r="1.8" fill="#fff" />
        <circle cx="118.8" cy="85.2" r="1.8" fill="#fff" />
      </>
    );
  return (
    <>
      {eyes}
      <path d="M92 98 q8 -4 16 0 q-2 8 -8 9 q-6 -1 -8 -9z" fill={INK} />
      <path d="M100 106 v4 M90 110 q5 6 10 0 q5 6 10 0" {...line} />
    </>
  );
}

export function DogFigure({ color = "butter", mood = "happy", className = "" }) {
  const { body, ear } = DOG_COLORS[color] ?? DOG_COLORS.butter;
  return (
    <svg viewBox="0 0 200 210" aria-hidden="true" className={`dog_figure ${className}`}>
      <ellipse cx="100" cy="200" rx="64" ry="8" fill={INK} opacity=".13" />
      <path className="dog_tail" d="M132 180 C158 176 170 156 161 132" fill="none" stroke={body} strokeWidth="13" strokeLinecap="round" />
      <path d="M60 199 C54 160 66 124 100 122 C134 124 146 160 140 199 Z" fill={body} />
      <path d="M89 146 q11 9 22 0 q-3 20 -11 25 q-8 -5 -11 -25z" fill="#fff" opacity=".5" />
      <path d="M66 186 q4 -16 18 -19 M134 186 q-4 -16 -18 -19 M86 170 V197 M114 170 V197 M80 198 h10 M110 198 h10" {...line} />
      <rect x="56" y="44" width="88" height="86" rx="40" fill={body} />
      <path d="M62 58 C40 55 31 92 43 112 C51 125 66 113 66 92 Z" fill={ear} />
      <path d="M138 58 C160 55 169 92 157 112 C149 125 134 113 134 92 Z" fill={ear} />
      <path d="M93 47 q4 -9 8 -1 q4 -7 8 0" {...line} />
      <path d="M68 128 Q100 144 132 128" stroke="#FF5C9A" strokeWidth="8" fill="none" strokeLinecap="round" />
      <circle cx="100" cy="141" r="6.5" fill="#E7C277" stroke={INK} strokeWidth="2" />
      <circle cx="72" cy="104" r="7" fill="#FF8FB8" opacity=".55" />
      <circle cx="128" cy="104" r="7" fill="#FF8FB8" opacity=".55" />
      <ellipse cx="100" cy="106" rx="19" ry="13" fill="#fff" opacity=".42" />
      <Face mood={mood} />
    </svg>
  );
}
