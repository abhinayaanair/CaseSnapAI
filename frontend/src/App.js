// src/App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import { AboutUs } from "./pages/AboutUs";
import { WhatWeDo } from "./pages/WhatWeDo";
import { GetInvolved } from "./pages/GetInvolved";
import { KnowledgeCorner } from "./pages/KnowledgeCorner";
import Chat from "./pages/Chat";
import Login from "./pages/Login";
import  SignUp  from "./pages/SignUp"; // Import Desktop as a named import
import Desktop from "./pages/Desktop";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about-us" element={<AboutUs />} />
        <Route path="/what-we-do" element={<WhatWeDo />} />
        <Route path="/get-involved" element={<GetInvolved />} />
        <Route path="/knowledge-corner" element={<KnowledgeCorner />} />
        
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<SignUp />} /> 
        <Route path="/casesnap" element={<Desktop />} /> 
      
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </Router>
  );
}

export default App;
