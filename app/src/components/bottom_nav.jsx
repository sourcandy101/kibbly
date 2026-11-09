import { pathTo } from "../logic/routes.js";

const TABS = [
  { label: "Today", target: "home", matches: ["home"] },
  { label: "Dogs", target: "dogs", matches: ["dogs", "dog_new", "dog_edit", "schedule"] },
  { label: "Calling order", target: "calling_order", matches: ["calling_order"] },
];

export default function BottomNav({ current }) {
  return (
    <nav className="bottom_nav" aria-label="Main">
      {TABS.map((tab) => {
        const active = tab.matches.includes(current);
        return (
          <a
            key={tab.target}
            href={pathTo(tab.target)}
            className={active ? "nav_link nav_link_active" : "nav_link"}
            aria-current={active ? "page" : undefined}
          >
            {tab.label}
          </a>
        );
      })}
    </nav>
  );
}
