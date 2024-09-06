import React, { useState } from 'react';
import axios from 'axios';
import '../styles/chat.css';
import '../styles/render.css';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [responses, setResponses] = useState([]);
  const [showDownloadButton, setShowDownloadButton] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return; // Prevent sending empty messages

    if (message.trim().toLowerCase() === 'end') {
      setMessage('');
      try {
        const response = await axios.post('http://localhost:5000/chat', { message });
        if (response.data.download_link) {
          setShowDownloadButton(true); // Show download button when "end" is typed
        }
      } catch (error) {
        console.error("Error sending message:", error);
      }
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/chat', { message });
      if (response.data.response) {
        setResponses([...responses, { user: message, bot: response.data.response }]);
        setMessage('');
      }
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent the default behavior of Enter key
      handleSend();
    }
  };

  return (
    <div className="mainchat">
      <div className="leftbar">
        <a href="/"><i className="fa-solid fa-house"></i></a>
        <div className="welcome-text">
          Welcome to CaseSnap AI, your smart legal assistant! I'm here to
          help simplify your legal journey by gathering key details and
          organizing your case information in a clear and concise way. Together,
          we can streamline the legal process, saving you time and making sure
          your concerns are accurately conveyed to your legal team.
        </div>
      </div>
      <div className="chat-form">
        <div className="chat-box">
          {responses.map((res, index) => (
            <div key={index} className="chat-message">
              <div className="user-message">{res.user}</div>
              <div className="bot-message">{res.bot}</div>
            </div>
          ))}
        </div>
        <form onSubmit={(e) => { e.preventDefault(); handleSend(); }}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress} // Add onKeyPress event handler
            placeholder="Type your message..."
            required
          />
          <button type="submit">Send</button>
          {showDownloadButton && (
            <a 
              href="http://localhost:5000/download/casesnap_chat_log.pdf" 
              target="_blank" 
              rel="noopener noreferrer"
              download
              className="download-link"
            >
              <button type="button" className="joinus download">
                Download Chat Log PDF
              </button>
            </a>
          )}
        </form>
      </div>
    </div>
  );
};

export default Chat;
