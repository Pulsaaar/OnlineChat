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

const apiUrl = "http://localhost:8000";

function Register() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [telegram_id, setTgId] = useState('');

  const handleLoginRedirect = () => {
    navigate('/login'); // Переход к компоненту входа
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${apiUrl}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          telegram_id,
          is_active: true,
          is_superuser: false,
          is_verified: false
        }),
      });

      if (!response.ok) {
        throw new Error('Registration failed');
      }

      navigate('/login'); // Перенаправление на страницу входа после успешной регистрации
    } catch (error) {
      console.error('Registration failed:', error);
    }
  };

  return (
    <MDBContainer fluid>
      <MDBRow>
        <MDBCol sm='6'>
          <div className='d-flex flex-row ps-5 pt-5'>
            <MDBIcon fas icon="crow fa-3x me-3" style={{ color: '#709085' }} />
            <span className="h1 fw-bold mb-0">Logo</span>
          </div>

          <div className='d-flex flex-column justify-content-center h-custom-2 w-75 pt-4'>
            <h3 className="fw-normal mb-3 ps-5 pb-3" style={{ letterSpacing: '1px' }}>Register</h3>

            <MDBInput
              wrapperClass='mb-4 mx-5 w-100'
              label='Email address'
              id='email'
              type='email'
              size="lg"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <MDBInput
              wrapperClass='mb-4 mx-5 w-100'
              label='telegram_id'
              id='telegram_id'
              type='text'
              size="lg"
              value={telegram_id}
              onChange={(e) => setTgId(e.target.value)}
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
              Register
            </MDBBtn>
            <p className='ms-5'>
              Already have an account? <span onClick={handleLoginRedirect} style={{ cursor: 'pointer', color: 'blue' }}>Sign In</span>
            </p>
          </div>
        </MDBCol>

        <MDBCol sm='6' className='d-none d-sm-block px-0'>
          <img
            src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/img3.webp"
            alt="Register image"
            className="w-100"
            style={{ objectFit: 'cover', objectPosition: 'left' }}
          />
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
}

export default Register;
