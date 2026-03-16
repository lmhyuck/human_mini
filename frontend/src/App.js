import React from "react";
import { Routes, Route } from "react-router-dom";
import Map from "./pages/Map";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import FindId from "./pages/FindId";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Map />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/find-id" element={<FindId />} />
    </Routes>
  );
}

export default App;
