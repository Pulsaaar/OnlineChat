import React, { useState } from 'react';
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBIcon,
  MDBInput
} from 'mdb-react-ui-kit';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

const apiUrl = "http://localhost:8000";

function App() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(''); // добавлено состояние для ошибки
  const { saveToken } = useAuth();

  const handleRegisterRedirect = () => {
    navigate('/register');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // сброс ошибки при новом запросе

    try {
      const response = await fetch(`${apiUrl}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Invalid email or password');
      }

      const data = await response.json();
      saveToken(data.access_token); // сохранение токена
      navigate('/'); // переход на главную страницу
    } catch (error) {
      setError("Invalid email or password"); // установка сообщения об ошибке для пользователя
    }
  };

  return (
    <MDBContainer fluid>
      <MDBRow>
        <MDBCol sm='6'>
          <div className='d-flex flex-row ps-5 pt-5'>
            <MDBIcon fas icon="crow fa-3x me-3" style={{ color: '#709085' }}/>
            <span className="h1 fw-bold mb-0">Logo</span>
          </div>

          <div className='d-flex flex-column justify-content-center h-custom-2 w-75 pt-4'>
            <h3 className="fw-normal mb-3 ps-5 pb-3" style={{ letterSpacing: '1px' }}>Log in</h3>

            <MDBInput
              wrapperClass='mb-4 mx-5 w-100'
              label='Email address'
              id='username'
              type='email'
              size="lg"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <MDBInput
              wrapperClass='mb-4 mx-5 w-100'
              label='Password'
              id='password'
              type='password'
              size="lg"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <MDBBtn
              className="mb-4 px-5 mx-5 w-100"
              color='info'
              size='lg'
              onClick={handleSubmit}
            >
              Login
            </MDBBtn>

            {/* Отображение сообщения об ошибке */}
            {error && (
              <div className="text-danger text-center mx-5 mb-4">
                {error}
              </div>
            )}

            <p className='ms-5'>
              Don't have an account? <span onClick={handleRegisterRedirect} style={{ cursor: 'pointer', color: 'blue' }}>Register here</span>
            </p>
          </div>
        </MDBCol>

        <MDBCol sm='6' className='d-none d-sm-block px-0'>
          <img
            src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/img3.webp"
            alt="Login image"
            className="w-100"
            style={{ objectFit: 'cover', objectPosition: 'left' }}
          />
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
}

export default App;
