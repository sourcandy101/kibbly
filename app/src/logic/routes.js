// Small hash router, so the phone's back button works without another package.

import { useEffect, useState } from "react";

const PATHS = {
  home: () => "#/home",
  dogs: () => "#/dogs",
  dog_new: () => "#/dogs/new",
  dog_edit: (dogId) => `#/dogs/${dogId}`,
  schedule: (dogId) => `#/dogs/${dogId}/schedule`,
  calling_order: () => "#/calling_order",
};

export function parseRoute(hash) {
  const parts = hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  if (parts[0] === "calling_order") return { name: "calling_order" };
  if (parts[0] !== "dogs") return { name: "home" };
  if (parts.length === 1) return { name: "dogs" };
  if (parts[1] === "new") return { name: "dog_new" };
  return { name: parts[2] === "schedule" ? "schedule" : "dog_edit", dogId: parts[1] };
}

export function pathTo(name, dogId) {
  return PATHS[name](dogId);
}

export function go(name, dogId) {
  window.location.hash = pathTo(name, dogId);
}

export function useRoute() {
  const [route, setRoute] = useState(() => parseRoute(window.location.hash));
  useEffect(() => {
    const update = () => setRoute(parseRoute(window.location.hash));
    window.addEventListener("hashchange", update);
    return () => window.removeEventListener("hashchange", update);
  }, []);
  return route;
}
