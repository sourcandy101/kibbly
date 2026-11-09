// Stands in for the dog's photo until photo upload is linked to Firebase.
const TONES = ["tone_clay", "tone_moss", "tone_sky", "tone_plum"];

function toneFor(name) {
  const total = [...name].reduce((sum, letter) => sum + letter.charCodeAt(0), 0);
  return TONES[total % TONES.length];
}

export default function DogAvatar({ name }) {
  return (
    <span className={`avatar ${toneFor(name)}`} aria-hidden="true">
      {name.charAt(0).toUpperCase()}
    </span>
  );
}
