import { createContext, useState } from "react";
import i18n from "../i18n";

export const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
const [language, setLanguage] = useState("en");

const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    setLanguage(lng);
};

return (
    <LanguageContext.Provider value={{ language, changeLanguage }}>
    {children}
    </LanguageContext.Provider>
);
};
