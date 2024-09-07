import React from "react";
import "../style.css";
import "../styles/getinvolved.css";

export const GetInvolved = () => {
  return (
    <div className="maininv">
      <div className="home"><a href="/" className="homea">Home</a></div>
      <div className="leftdiv">
        <div className="heading">How We’re Making A Difference</div>
        <div className="getinv1">
          We are transforming the way legal information is gathered and presented. By using AI, we help users
          articulate their legal concerns clearly and ensure that lawyers receive accurate and well-organized
          information.
        </div>
        <div className="getinv2">
          Our platform simplifies complex legal information, allowing you to focus on what truly matters.
        </div>
        <div className="getinv3">
          Opt for CaseSnap AI to make legal services more approachable and less daunting. Our user-friendly
          technology ensures you can engage with the legal system smoothly and effectively.
        </div>
      </div>
      <div className="rightdiv">
        <div className="topimg"></div>
        <div className="bottomimg"></div>
      </div>

      {/* Add the glowing effect divs */}
      <div className="glow-top-left"></div>
      <div className="glow-bottom-right"></div>
    </div>
  );
};

export default GetInvolved;
