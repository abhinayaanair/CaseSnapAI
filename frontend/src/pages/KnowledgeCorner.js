import React, { useState, useEffect } from "react";
import "../style.css";  // Ensure this path is correct
import "../styles/knowledgecorner.css";
import legalData from "../legal.json"; // Adjust the path as necessary

export const KnowledgeCorner = () => {
    const [randomQA, setRandomQA] = useState({ question: '', answer: '' });

    useEffect(() => {
        // Function to get a random question and answer
        const getRandomQA = () => {
            const randomIndex = Math.floor(Math.random() * legalData.length);
            return legalData[randomIndex];
        };

        // Set initial question and answer
        setRandomQA(getRandomQA());

        // Set interval to update question and answer every 10 seconds
        const intervalId = setInterval(() => {
            setRandomQA(getRandomQA());
        }, 10000); // 10000 milliseconds = 10 seconds

        // Cleanup interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div>
            <div className="mainKnowledge">
                <div className="home"><a href="/" className="homea">Home</a></div>
                <div className="leftknowledge">
                    <br /><br /><br />
                    <div className="knowledgeClarityProgress">
                        Knowledge, Clarity, Progress
                    </div>
                    <div className="knowledgeImage">
                        {/* Background image styling goes here */}
                    </div>
                    <div className="readThis">Read This</div>
                    <div className="questionStatement">
                        We provide questions which actively change with provision to solutions
                    </div>
                </div>
               
                <div className="rightknowledge">
                    <div className="quesandans">
                        <div className="question">
                            {randomQA.question}
                        </div>
                        <div className="answer">
                            {randomQA.answer}
                        </div>
                    </div>
                </div>
            </div>

            <div className="bottom-column">
                <div className="frame29992"><div className="clear">Clear</div></div>
                <div className="frame3010"><div className="concise">Concise</div></div>
                <div className="frame30082"><div className="efficient">Efficient</div></div>
                <div className="frame30092"><div className="accurate">Accurate</div></div>
            </div>
        </div>
    );
};
