import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './LawyerChat.css';
import boyAvatar from './assets/boy.png';
import girlAvatar from './assets/girl.png';
import lawyerAvatar from './assets/lawyer.png';

function LawyerChat() {
    const [roomId, setRoomId] = useState('');
    const [username, setUsername] = useState('');
    const [gender, setGender] = useState('');
    const [messages, setMessages] = useState([]);
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

    useEffect(() => {
        // This effect will run only once on initial render
        fetch(`http://35.236.145.95:5000/?user=${gender}`, {
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
    }, []);


    // 定期获取消息
    useEffect(() => {
        const interval = setInterval(() => {
            fetch(`http://35.236.145.95:5000/lawyer?user=${gender}`, {
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
                message: message,
            };

            const newMessages = [...messages, payload];
            setMessages(newMessages);

            fetch('http://35.236.145.95:5000/lawyer', {
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

            <div className="container">
                <div className="intro">
                    <h1>律師聊天室</h1>
                    <p>暢談你心中的不快</p>
                </div>

                <div className="chat-section">
                    <div id="chat-box" className="chat-box">
                        {messages.map((msg, index) => {
                            // 确定头像图片
                            let avatar = null;
                            if (msg.sender === 'boy') {
                                avatar = boyAvatar;
                            } else if (msg.sender === 'girl') {
                                avatar = girlAvatar;
                            } else if (msg.sender === 'lawyer') {
                                avatar = lawyerAvatar;
                            }

                            // 确定消息的样式类名
                            let messageClass = '';
                            if (msg.sender === 'system') {
                                messageClass = 'system';
                            } else if (msg.sender === gender) {
                                messageClass = 'user';
                            } else {
                                messageClass = 'other';
                            }

                            return (
                                <div key={index} className={`chat-message ${messageClass}`}>
                                    {msg.sender !== 'system' && msg.sender !== gender && avatar && (
                                        <img src={avatar} alt={`${msg.sender} avatar`} className="avatar" />
                                    )}
                                    <div className="message-content">
                                        {msg.text || msg.message}
                                    </div>
                                </div>
                            );
                        })}
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
                        <button id="back-button" onClick={handleBack}>
                            返回
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default LawyerChat;
