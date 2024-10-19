import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Chat from './Chat';
import Login from './Login';
import LawyerChat from './LawyerChat';
import './styles.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/lawyer-chat" element={<LawyerChat />} />
      </Routes>
    </Router>
  );
}

export default App;
