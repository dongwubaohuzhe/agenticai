'use client';

import React, { useState, useRef, useEffect } from 'react';
import { FiSend, FiUser, FiWifi, FiAlertCircle } from 'react-icons/fi';
import ReactMarkdown from 'react-markdown';
import { useStore } from '../lib/store';

interface ChatInterfaceProps {
  flightInfo: {
    flightNumber: string;
    origin: string;
    destination: string;
    airline: string;
    date: string;
    departureTime: string;
    status: string;
  };
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ flightInfo }) => {
  const [input, setInput] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [localMessages, setLocalMessages] = useState<Array<{role: string, content: string}>>([
    {
      role: 'assistant',
      content: `Welcome! I'm your flight assistant for flight ${flightInfo.flightNumber} from ${flightInfo.origin} to ${flightInfo.destination}. How can I help you today?`
    }
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { conversations, currentConversationId, addMessage } = useStore();

  // Get current conversation
  const currentConversation = currentConversationId
    ? conversations.find(c => c.id === currentConversationId)
    : null;

  // Initialize conversation if needed
  useEffect(() => {
    if (!currentConversationId && flightInfo) {
      // If we can't access the store, we'll just use local state
      console.log("Using local messages only - no conversation ID found");
    }
  }, [currentConversationId, flightInfo, addMessage]);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [localMessages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!input.trim()) return;
    setIsSending(true);

    // Add user message to local state
    const userMessage = {
      role: 'user',
      content: input
    };
    setLocalMessages(prev => [...prev, userMessage]);
    setInput('');

    // Simulate AI response with flight information
    setTimeout(() => {
      const responseContent = generateResponse(input, flightInfo);
      setLocalMessages(prev => [...prev, {
        role: 'assistant',
        content: responseContent
      }]);
      setIsSending(false);
    }, 1000);

    // If store is available, also add message there
    if (currentConversationId) {
      try {
        await addMessage({
          role: 'user',
          content: input,
        });
      } catch (err) {
        console.error("Failed to add message to store:", err);
      }
    }
  };

  const generateResponse = (query: string, flightInfo: ChatInterfaceProps['flightInfo']) => {
    const lowerQuery = query.toLowerCase();

    if (lowerQuery.includes('time') || lowerQuery.includes('when')) {
      return `Flight ${flightInfo.flightNumber} is scheduled to depart at ${flightInfo.departureTime} on ${flightInfo.date}.`;
    }

    if (lowerQuery.includes('delay') || lowerQuery.includes('on time')) {
      return `Currently, your flight ${flightInfo.flightNumber} is ${flightInfo.status.toLowerCase()}. I'll notify you if there are any changes.`;
    }

    if (lowerQuery.includes('airline')) {
      return `You're flying with ${flightInfo.airline} on flight ${flightInfo.flightNumber}.`;
    }

    if (lowerQuery.includes('arrive') || lowerQuery.includes('airport')) {
      return `For your flight from ${flightInfo.origin} to ${flightInfo.destination}, we recommend arriving at the airport at least 2 hours before your scheduled departure time of ${flightInfo.departureTime}.`;
    }

    return `I'm here to help with your ${flightInfo.airline} flight ${flightInfo.flightNumber} from ${flightInfo.origin} to ${flightInfo.destination}. Is there anything specific you'd like to know?`;
  };

  // Use messages from store if available, otherwise use local state
  const messagesToDisplay = currentConversation?.messages || localMessages;

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messagesToDisplay.map((message, index) => (
          message.role !== 'system' && (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3/4 p-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white rounded-tr-none'
                    : 'bg-gray-100 dark:bg-gray-800 rounded-tl-none'
                }`}
              >
                <ReactMarkdown>
                  {message.content}
                </ReactMarkdown>
              </div>
            </div>
          )
        ))}
        {isSending && (
          <div className="flex justify-start">
            <div className="max-w-3/4 p-3 bg-gray-100 dark:bg-gray-800 rounded-lg rounded-tl-none">
              <div className="flex space-x-2 items-center">
                <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about your flight..."
            className="flex-1 p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isSending}
          />
          <button
            type="submit"
            disabled={!input.trim() || isSending}
            className="bg-blue-500 text-white p-2 rounded-lg disabled:opacity-50"
          >
            <FiSend />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
