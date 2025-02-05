import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import HomePage from "./Home/HomePage";
import AdminPanel from "./Admin/AdminPanel";

const Router = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="AdminPanel" element={<AdminPanel />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default Router;
