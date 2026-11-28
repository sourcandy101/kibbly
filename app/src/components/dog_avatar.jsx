import { DOG_COLORS, DogFigure } from "./dog_figure.jsx";

// The dog character in a round tile of its color. Stands in for a photo until uploads are linked.
export default function DogAvatar({ color = "butter", mood = "happy", size = "medium" }) {
  return (
    <span className={`avatar avatar_${size}`} style={{ background: DOG_COLORS[color]?.tint }} aria-hidden="true">
      <DogFigure color={color} mood={mood} />
    </span>
  );
}
