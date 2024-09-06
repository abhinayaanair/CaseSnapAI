import React, { useState } from 'react';
import axios from 'axios';
import '../styles/login.css';
import { useNavigate } from 'react-router-dom';

export const SignUp = ({ className, ...props }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/signup', {
        email,
        password,
      });
      if (response.status === 201) {
        navigate('/casesnap');
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.message);
        if (error.response.status === 400) {
          navigate('/signup');
        }
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
        <form className="authform" onSubmit={handleSignup}>
          <h2>Sign Up</h2>
          <label>
            Email:
            <input  className="authinput" 
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder='Enter your email...'
            />
          </label>
          <label>
            Password:
            <input  className="authinput" 
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder='Enter your password...'
            />
          </label>
          <button type="submit" className='authbutton'>Sign Up</button>
          {message && <p>{message}</p>}
        </form>
        <a href="/login"><button class="authbutton signup-button">Go to Login</button>   </a>
        <div className="black-design"></div>
      </div>
    </div>
  );
};

export default SignUp;
