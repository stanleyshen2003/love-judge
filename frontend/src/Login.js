import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login() {
    const [roomId, setRoomId] = useState('');
    const [name, setName] = useState('');
    const [gender, setGender] = useState('boy');
    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault(); // 防止表单自动提交

        if (roomId.trim() && name.trim() && gender) {
            // 将信息保存到本地存储或状态管理
            localStorage.setItem('roomId', roomId.trim());
            localStorage.setItem('username', name.trim());
            localStorage.setItem('gender', gender);

            // 根据性别跳转到不同的聊天页面
            navigate('/chat');
        }
    };

    return (
        <div className="login-container">
            <h1>戀愛裁判 - 登入</h1>
            <form id="login-form" onSubmit={handleSubmit}>
                <label htmlFor="room-id">房間 ID:</label>
                <input
                    type="text"
                    id="room-id"
                    required
                    value={roomId}
                    onChange={(e) => setRoomId(e.target.value)}
                />

                <label htmlFor="name">你的名字:</label>
                <input
                    type="text"
                    id="name"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />

                <label htmlFor="gender">性別:</label>
                <select
                    id="gender"
                    required
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                >
                    <option value="boy">Boy</option>
                    <option value="girl">Girl</option>
                </select>

                <button type="submit">進入房間</button>
            </form>
        </div>
    );
}

export default Login;
