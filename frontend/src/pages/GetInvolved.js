import React from "react";
import "../style.css";
import "../styles/getinvolved.css";

export const GetInvolved = () => {
  return (
    <div className="desktop">
      <div className="overlap-wrapper">
        <div className="overlap">
          <div className="overlap-group">
            <div className="works">
              <div className="frame">
                <p className="how-we-re-making-a">How We’re Making A Difference</p>
                <p className="text-wrapper">
                  We are transforming the way legal information is gathered and presented. By using AI, we help users
                  articulate their legal concerns clearly and ensure that lawyers receive accurate and well-organized
                  information.
                </p>
                <div className="div-wrapper">
                  <p className="div">
                    Our platform simplifies complex legal information, allowing you to focus on what truly matters.
                  </p>
                </div>
                <div className="div-wrapper">
                  <p className="div">
                    Opt for CaseSnap AI to make legal services more approachable and less daunting. Our user-friendly
                    technology ensures you can engage with the legal system smoothly and effectively.
                  </p>
                </div>
                <div className="deusa-logo" />
              </div>
              <div className="group">
                <div className="overlap-group-2">
                  <img className="vector" alt="Vector" src="vector.svg" />
                  <div className="image-wrapper">
                    <img className="image" alt="Image" src="image.png" />
                  </div>
                  <div className="img-wrapper">
                    <img className="img" alt="Image" src="image-2.png" />
                  </div>
                </div>
              </div>
            </div>
            <img className="designs" alt="Designs" src="designs.svg" />
            <img className="designs-2" alt="Designs" src="image.svg" />
            <img className="hero-shadow" alt="Hero shadow" src="hero-shadow.png" />
            <img className="hero-shadow-2" alt="Hero shadow" src="hero-shadow-2.png" />
          </div>
          <img className="surface" alt="Surface" src="surface-1.png" />
          <div className="text-wrapper-2">Home</div>
        </div>
      </div>
    </div>
  );
};

export default GetInvolved;
