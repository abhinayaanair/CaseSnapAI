import React from "react";
import "../style.css";
import "../styles/aboutus.css";

export const AboutUs = () => { 
  return (
   
    <div className="desktop">
       <div className="home"><a href="/" className="homea">Home</a></div>
      <div className="about-us-section">
        <div className="about-us-image"></div>
        <div className="text-container">
          <div className="title-wrapper">
            <div className="about-title">About Us</div>
            <div className="line"></div>
          </div>
          <div className="subtitle">Revolutionizing Legal Accessibility</div>
          <p className="description">
            We are committed to enhancing the accessibility and efficiency of the legal process. Our AI-driven platform 
            interacts with users to gather and simplify their legal case details into clear, concise documents, making 
            it easier for lawyers to understand and act upon them.
          </p>
        </div>
      </div>

      <div className="glow-top-left"></div>
      <div className="glow-bottom-right"></div>
    </div>
  );
};
