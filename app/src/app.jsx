import { useCallback, useEffect, useState } from "react";
import { getCurrentUser, loadHomeData, signOut } from "./data/store.js";
import { go, useRoute } from "./logic/routes.js";
import BottomNav from "./components/bottom_nav.jsx";
import CallingOrderScreen from "./screens/calling_order_screen.jsx";
import DogFormScreen from "./screens/dog_form_screen.jsx";
import DogsScreen from "./screens/dogs_screen.jsx";
import HomeScreen from "./screens/home_screen.jsx";
import LoginScreen from "./screens/login_screen.jsx";
import ScheduleScreen from "./screens/schedule_screen.jsx";

export default function App() {
  const route = useRoute();
  const [user, setUser] = useState(undefined);
  const [data, setData] = useState(null);

  const refresh = useCallback(async () => {
    setData(await loadHomeData());
  }, []);

  useEffect(() => {
    getCurrentUser().then(setUser);
  }, []);

  useEffect(() => {
    if (user) refresh();
  }, [user, refresh]);

  // Start each new screen at the top, as a phone user expects.
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [route.name, route.dogId]);

  if (user === undefined) return null;
  if (!user) return <LoginScreen onSignedIn={setUser} />;
  if (!data) return null;

  const handleSignOut = async () => {
    await signOut();
    setUser(null);
    go("home");
  };

  const shared = { data, refresh };
  let screen;
  switch (route.name) {
    case "dogs":
      screen = <DogsScreen {...shared} />;
      break;
    case "dog_new":
      screen = <DogFormScreen {...shared} />;
      break;
    case "dog_edit":
      screen = <DogFormScreen {...shared} key={route.dogId} dogId={route.dogId} />;
      break;
    case "schedule":
      screen = <ScheduleScreen {...shared} key={route.dogId} dogId={route.dogId} />;
      break;
    case "calling_order":
      screen = <CallingOrderScreen {...shared} />;
      break;
    default:
      screen = <HomeScreen {...shared} user={user} onSignOut={handleSignOut} />;
  }

  return (
    <div className="shell">
      <p className="preview_banner">Preview: your data stays in this browser</p>
      <main className="page">{screen}</main>
      <BottomNav current={route.name} />
    </div>
  );
}
