import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import LoginPage from "./loginPage";
import Activate2FA from "./activate_2fa";
import axios from "axios";
import Validate_TOTP from "./validate_totp";

axios.defaults.baseURL = "http://localhost:8000/";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="" element={<LoginPage />} />
        <Route path="/activate_2fa" element={<Activate2FA />} />
        <Route path="/validate_totp" element={<Validate_TOTP />} />
      </Routes>
    </BrowserRouter>
  );
};

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<App />);
