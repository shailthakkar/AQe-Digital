import React from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "../src/components/Admin/Sidebar";
import NavBar from "../src/components/NavBar";

const Layout = () => {
  const location = useLocation();

  // Check if the current route is the Home Page or Player Dashboard page
  const isHomePage = location.pathname === "/";
  const isPlayerDashboard = location.pathname.startsWith("/player/");

  return (
    <div className="layout">
      <NavBar />
      <div style={{ display: "flex" }}>
        {/* Conditionally render Sidebar based on the route */}
        {!isHomePage && !isPlayerDashboard && <Sidebar />}
        <div style={{ flex: 1 }}>
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout;
