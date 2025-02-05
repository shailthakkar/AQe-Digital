import React, { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import HomePage from "./components/Home/HomePage";
import AdminPanel from "./components/Admin/AdminPanel";
import PlayerDashboard from "./components/PlayerDashboard";
import { useTranslation } from "react-i18next"; // Import useTranslation
import i18n from "./i18n";
import "./App.css";

const LanguageSelector = ({ onSelect }) => {
  const { t } = useTranslation(); // Use t here
  return (
    <div className="language-popup bg-gray-800">
      <h2>{t("select_language")}</h2>
      <button className="bg-green-600" onClick={() => onSelect("en")}>English</button>
      <button className="bg-green-600" onClick={() => onSelect("es")}>Español</button>
      <button className="bg-green-600" onClick={() => onSelect("ja")}>日本語</button>
    </div>
  );
};

const App = () => {
  const { t } = useTranslation(); // Use t here
  const [languageSelected, setLanguageSelected] = useState(false);

  const handleLanguageChange = (lng) => {
    i18n.changeLanguage(lng);
    setLanguageSelected(true);
  };

  return (
    <div>
      {!languageSelected && <LanguageSelector onSelect={handleLanguageChange} />}

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="/admin" element={<AdminPanel />} />
            <Route path="/player/:playerName" element={<PlayerDashboard />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default App;