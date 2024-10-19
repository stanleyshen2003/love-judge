import React from 'react';

function Message({ message, selfSender }) {
    let className = 'chat-message ';
    if (message.sender === 'system' || message.sender === 'judge') {
        className += 'system';
    } else if (message.sender === selfSender) {
        className += 'user';
    } else {
        className += 'other';
    }

    return <div className={className}>{message.text}</div>;
}

export default Message;
