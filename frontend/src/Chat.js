import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './styles.css';
import boyAvatar from './assets/boy.png';
import girlAvatar from './assets/girl.png';
import judgeAvatar from './assets/judge.png';

function Chat() {
    const [roomId, setRoomId] = useState('');
    const [username, setUsername] = useState('');
    const [gender, setGender] = useState('');
    const [messages, setMessages] = useState([]);
    const [messageInput, setMessageInput] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        // 从本地存储获取信息
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
        fetch(`http://127.0.0.1:5000/?user=${gender}`, {
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
            fetch(`http://127.0.0.1:5000/?user=${gender}`, {
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
            setMessageInput('');
            fetch('http://127.0.0.1:5000/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            })
                .then((response) => response.json())
                .then((data) => {
                    // setMessageInput('');
                    setMessages(data.messages);
                })
                .catch((error) => {
                    console.error('Error sending message:', error);
                });
        }
    };

    const handleLawyerButtonClick = () => {
        navigate('/lawyer-chat');
    };

    return (
        <div className="chat-container">
            <div className="header">
                戀愛裁判 - Love Judge ({username})
            </div>
            <div className="content">
                <div className="intro">
                    <h1>戀愛問題解決！</h1>
                    <p>房間 ID: {roomId}</p>
                </div>
                {/* 聊天区域 */}
                <div className="chat-section">
                    <div id="chat-box" className="chat-box">
                        {messages.map((msg, index) => {
                            // 确定头像图片
                            let avatar = null;
                            if (msg.sender === 'boy') {
                                avatar = boyAvatar;
                            } else if (msg.sender === 'girl') {
                                avatar = girlAvatar;
                            } else if (msg.sender === 'judge') {
                                avatar = judgeAvatar;
                            }

                            // 确定消息的样式类名
                            let messageClass = '';
                            if (msg.sender === 'system') {
                                messageClass = 'system';
                            } else if (msg.sender === gender) {
                                messageClass = 'user';
                            } else if (msg.sender === 'judge') {
                                messageClass = 'judge';
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
                        <button id="lawyer-button" onClick={handleLawyerButtonClick}>
                            Lawyer
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Chat;
