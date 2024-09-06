import React from "react";
import "../style.css";
import "../styles/whatwedo.css";

export const WhatWeDo = () => {
  return (
    <div className="desktop">
      <div className="overlap-wrapper">
        <div className="overlap">
          <div className="overlap-group">
            <div className="frame">
              <div className="text-wrapper">Our Mission</div>
              <p className="div">
                Our mission is to democratize access to legal services by leveraging AI to assist in the preparation and
                understanding of legal cases. We strive to reduce the time and cost involved in legal proceedings,
                making the legal process more transparent and less intimidating for everyone.
              </p>
            </div>
            <div className="objectives-functions">
              <div className="frame-2">
                <div className="text-wrapper">Objectives & Functions</div>
                <p className="div">
                  Our goal is to streamline the initial data collection process and ensure that the information gathered
                  is both comprehensive and relevant. We then present this data in a simplified, clear format, making it
                  easy for lawyers to review and act upon efficiently.
                </p>
              </div>
            </div>
            <img className="hero-shadow" alt="Hero shadow" src="hero-shadow.png" />
            <img className="img" alt="Image" src="image.png" />
            <div className="text-wrapper-2">Home</div>
          </div>
          <div className="frame-3">
            <div className="text-wrapper">
              Take A<br /> Pledge!
            </div>
            <div className="div-wrapper">
              <div className="text-wrapper-3">Support Us</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WhatWeDo;
