import React from "react";
import "../style.css";
import "../styles/aboutus.css";

export const AboutUs = () => { 
  return (
    <div className="desktop">
      <div className="overlap-wrapper">
        <div className="overlap">
          <div className="overlap-group">
            <div className="about-us">
              <div className="group">
                <div className="image-wrapper">
                  <img className="image" alt="Image" src="image.png" />
                </div>
              </div>
              <div className="frame">
                <div className="div">
                  <div className="text-wrapper">About Us</div>
                  <img className="line" alt="Line" src="line-171.svg" />
                </div>
                <div className="text-wrapper-2">Revolutionizing Legal Accessibility</div>
                <p className="p">
                  We are committed to enhancing the accessibility and efficiency of the legal process. Our AI-driven
                  platform interacts with users to gather and simplify their legal case details into clear, concise
                  documents, making it easier for lawyers to understand and act upon them.
                </p>
              </div>
            </div>
            <img className="hero-shadow" alt="Hero shadow" src="hero-shadow.png" />
            <img className="img" alt="Hero shadow" src="hero-shadow-2.png" />
          </div>
          <div className="text-wrapper-3">Home</div>
        </div>
      </div>
    </div>
  );
};
