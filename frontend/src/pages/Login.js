import React, { useState } from 'react';
import axios from 'axios';
import '../styles/login.css';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

export const Login = ({ className, ...props }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate(); // Initialize useNavigate

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', {
        email,
        password,
      });
      if (response.status === 200) {
        navigate('/casesnap'); // Redirect to /casesnap on successful login
      }
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.message);
      } else {
        setMessage('An unexpected error occurred');
      }
    }
  };

  return (
    <div className="mainSignUp">
      <div className="background-image">
        <div className="whitetext">Together, we  <br></br>can redfine justice</div>
       
      </div>
      <div className="form-container">
        <form className="authform" onSubmit={handleLogin}>
          <h2>Log In</h2>
          <label>
            Email:
            <input className="authinput" 
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder='Enter your email...'
            />
          </label>
          <label>
            Password:
            <input className="authinput" 
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder='Enter your password...'
            />
          </label>
          <button className="authbutton" type="submit">Continue</button>
          {message && <p >{message}</p>}
         
         
        </form>
        <a href="/signup"><button class="authbutton signup-button">Go to SignUp</button>   </a>
        <div className="black-design"></div>
        <div className="black-design"></div>
      </div>
    </div>
  );
};

export default Login;
