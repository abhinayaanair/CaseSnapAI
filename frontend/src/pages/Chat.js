import React, { useState } from 'react';
import axios from 'axios';
import '../styles/chat.css';
import '../styles/render.css';

const LoadingIndicator = () => (
  <div className="loading-container">
    <div className="loading-spinner"></div>
    <p>Loading...</p>
  </div>
);

const Chat = () => {
  const [message, setMessage] = useState('');
  const [responses, setResponses] = useState([]);
  const [downloadUrl, setDownloadUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;

    setLoading(true);

    try {
      const response = await axios.post('https://casesnapai.onrender.com/chat', { message });

      console.log("Response data:", response.data); // Debugging line

      if (message.trim().toLowerCase() === 'end') {
        if (response.data.download_link) {
          setDownloadUrl(response.data.download_link);
        }
      } else if (response.data.response) {
        setResponses([...responses, { user: message, bot: response.data.response }]);
        setMessage('');
      }

    } catch (error) {
      console.error("Error sending message:", error);
    }

    setLoading(false);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
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
            onKeyPress={handleKeyPress}
            placeholder="Type 'end' to download chat log."
            required
          />
          <button type="submit" disabled={loading}>Send</button>
          {loading && <LoadingIndicator />}
          {downloadUrl && (
            <a 
              href={downloadUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              download="casesnap_chat_log.jpg"
              className="download-link"
            >
              <button type="button" className="joinus download">
                Download Chat Log Image
              </button>
            </a>
          )}
        </form>
      </div>
    </div>
  );
};

export default Chat;
