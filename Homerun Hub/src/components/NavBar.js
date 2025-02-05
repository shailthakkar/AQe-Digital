import React from "react";
import { Link } from "react-router-dom"; // Import Link
import logo from "../components/logo.png";
import { useTranslation } from "react-i18next";

const NavBar = () => {
  const { t } = useTranslation();
  return (
    <nav className="bg-customGray text-white shadow-md top-0 left-0 w-full z-10">
      <div className="container mx-auto flex items-center justify-start p-2">
        <h1 className="text-3xl font-bold text-center text-white p-4 rounded-lg shadow-lg tracking-wider font-mono flex items-center space-x-2">
          <Link to="/" className="flex">
            {t("HomerunHub")}
            <img
              src={logo}
              alt="Homerun Hub logo"
              className="h-8 w-8 object-contain"
            />
          </Link>
        </h1>
      </div>
    </nav>
  );
};

export default NavBar;
