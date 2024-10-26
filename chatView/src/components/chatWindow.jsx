import React, { useState, useEffect } from "react";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBBtn,
  MDBTypography,
  MDBTextArea,
  MDBCardHeader,
} from "mdb-react-ui-kit";
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';

export default function App() {
  const navigate = useNavigate();
  const [me, setMe] = useState(null);
  const [users, setUsers] = useState([]);
  const [messages, setMessages] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [newMessage, setNewMessage] = useState("");
  const { token, saveToken } = useAuth();
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    if (!token) {
      navigate('/login');
    }
  }, [token, navigate]);

  const sendMessage = () => {
    if (socket && newMessage.trim() !== "") {
      const message = {
        sender_id: me.id,
        recipient_id: selectedUser.id,
        content: newMessage,
      };

      socket.send(JSON.stringify(message));
      setNewMessage("");

      setMessages(prevMessages => [...prevMessages, message]);
    }
  };

  useEffect(() => {
    async function fetchUsers() {
      const response = await fetch("http://localhost:8000/chat/users");
      const data = await response.json();
      setUsers(data);

      const response_me = await fetch("http://localhost:8000/chat/me", {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        },
      });
      const data_me = await response_me.json();
      setMe(data_me);
    }
    fetchUsers();
  }, []);

  useEffect(() => {
    if (me) {
      const ws = new WebSocket(`ws://localhost:8000/chat/ws/${me.id}`);
      setSocket(ws);

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.sender_id === selectedUser?.id) {
          setMessages((prevMessages) => [...prevMessages, data]);
        }
      };

      return () => ws.close();
    }
  }, [me, selectedUser]);

  useEffect(() => {
    if (selectedUser) {
      async function fetchMessages() {
        const response = await fetch(
          `http://localhost:8000/messages/?recipient_id=${selectedUser.id}`,
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${token}`
            },
          }
        );
        const data = await response.json();
        setMessages(data);
      }
      fetchMessages();
    }
  }, [selectedUser]);

  const handleUserClick = (user) => {
    setSelectedUser(user);
  };  
  
  const logout = () => {
    saveToken(null);
  };


  return (
    <MDBContainer fluid className="py-5" style={{ backgroundColor: "#eee", height: "100vh" }}>
      <MDBRow>
        <MDBCol md="6" lg="5" xl="4" className="mb-4 mb-md-0 d-flex flex-column" style={{ height: "100vh" }}>
          <h5 className="font-weight-bold mb-3 text-center text-lg-start">Members</h5>
          <MDBCard className="flex-grow-1 d-flex flex-column">
            <MDBCardBody style={{ overflowY: "auto", maxHeight: "calc(85vh - 60px)" }}>
              <MDBTypography listUnStyled className="mb-0">
                {users.map((user) => (
                  <li
                    key={user.id}
                    className="p-2 border-bottom mb-2"
                    style={{ backgroundColor: selectedUser?.id === user.id ? "#ddd" : "#eee" }}
                    onClick={() => handleUserClick(user)}
                  >
                    <div className="d-flex justify-content-between pt-1">
                      <p className="fw-bold mb-0">{user.username}</p>
                    </div>
                  </li>
                ))}
              </MDBTypography>
            </MDBCardBody>

            {/* Блок с кнопкой и email, зафиксирован внизу */}
            <div className="p-3 border-top">
              {me && <p className="mb-1">Logged in as: {me.email}</p>}
              <MDBBtn color="danger" size="sm" onClick={logout} className="w-100">
                Logout
              </MDBBtn>
            </div>
          </MDBCard>
        </MDBCol>

        <MDBCol md="6" lg="7" xl="8" style={{ height: "90vh", display: "flex", flexDirection: "column" }}>
          <MDBTypography listUnStyled style={{ flexGrow: 1, overflowY: "auto" }}>
            {messages.map((message, index) => (
              <li
                key={index}
                className={`d-flex mb-4 ${message.sender_id === selectedUser?.id ? "justify-content-start" : "justify-content-end"}`}
              >
                <MDBCard className="w-75">
                  <MDBCardHeader className="d-flex justify-content-between p-3">
                    <p className="fw-bold mb-0">{message.sender_id === selectedUser?.id ? selectedUser.username : "You"}</p>
                  </MDBCardHeader>
                  <MDBCardBody>
                    <p className="mb-0">{message.content}</p>
                  </MDBCardBody>
                </MDBCard>
              </li>
            ))}
          </MDBTypography>

          {selectedUser && (
            <div className="d-flex align-items-center mt-3">
              <MDBTextArea
                label="Message"
                id="textArea"
                rows={4}
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                className="flex-grow-1 me-2"
                style={{ resize: "none", backgroundColor: "#cce4ff" }}
              />
              <MDBBtn
                color="info"
                style={{ height: "100%", padding: "0 1rem" }}
                onClick={sendMessage}
              >
                Send
              </MDBBtn>
            </div>
          )}
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
}
