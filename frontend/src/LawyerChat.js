import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './LawyerChat.css';

function LawyerChat() {
    const [roomId, setRoomId] = useState('');
    const [username, setUsername] = useState('');
    const [gender, setGender] = useState('');
    const [messages, setMessages] = useState([
        { text: '歡迎來到律師聊天室，有什麼想詢問的呢？', sender: 'system' },
    ]);
    const [messageInput, setMessageInput] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const storedRoomId = localStorage.getItem('roomId');
        const storedUsername = localStorage.getItem('username');
        const storedGender = localStorage.getItem('gender');

        if (storedRoomId && storedUsername && storedGender) {
            setRoomId(storedRoomId);
            setUsername(storedUsername);
            setGender(storedGender);
        } else {
            navigate('/login');
        }
    }, [navigate]);

    // 定期获取消息
    useEffect(() => {
        const interval = setInterval(() => {
            fetch(`http://35.194.188.10:5000/?user=${gender}`, {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' },
            })
                .then((response) => response.json())
                .then((data) => {
                    setMessages(data.messages);
                })
                .catch((error) => {
                    console.error('Error fetching messages:', error);
                });
        }, 3000);
        return () => clearInterval(interval);
    }, [gender]);

    // 发送消息
    const sendMessage = () => {
        const message = messageInput.trim();
        if (message) {
            const payload = {
                sender: gender, // 使用性别作为发送者
                messages: {
                    sender: gender, // 使用性别作为发送者
                    text: message,
                },
            };

            fetch('http://35.194.188.10:5000/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            })
                .then((response) => response.json())
                .then((data) => {
                    setMessageInput('');
                    setMessages(data.messages);
                })
                .catch((error) => {
                    console.error('Error sending message:', error);
                });
        }
    };

    // 返回主聊天室
    const handleBack = () => {
        navigate('/chat');
    };

    return (
        <div className="lawyer-chat">
            <div className="header">
                房間 ID: <span>{roomId}</span>
            </div>

            <div className="container">
                <div className="intro">
                    <h1>律師聊天室</h1>
                    <p>與律師討論你的問題！</p>
                    <p>
                        你好，<span>{username}</span>！
                    </p>
                </div>

                <div className="chat-section">
                    <div id="chat-box" className="chat-box">
                        {messages.map((msg, index) => (
                            <div
                                key={index}
                                className={`chat-message ${msg.sender === 'system'
                                    ? 'system'
                                    : msg.sender === gender
                                        ? 'user'
                                        : 'other'
                                    }`}
                            >
                                {msg.sender !== 'system' && msg.sender !== gender
                                    ? `${msg.sender}: `
                                    : ''}
                                {msg.text}
                            </div>
                        ))}
                    </div>

                    <div className="input-section">
                        <div className="input-wrapper">
                            <input
                                type="text"
                                id="message-input"
                                placeholder="輸入訊息..."
                                value={messageInput}
                                onChange={(e) => setMessageInput(e.target.value)}
                                onKeyPress={(e) => {
                                    if (e.key === 'Enter') sendMessage();
                                }}
                            />
                            <button id="send-button" onClick={sendMessage}>
                                發送
                            </button>
                        </div>
                        <button
                            className="back-button"
                            id="back-button"
                            onClick={handleBack}
                        >
                            返回
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LawyerChat;
