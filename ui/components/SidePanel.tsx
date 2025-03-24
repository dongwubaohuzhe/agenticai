'use client';

import React, { useState } from 'react';
import { FiPlusCircle, FiMenu, FiMessageSquare, FiX } from 'react-icons/fi';
import { useStore, Conversation } from '../lib/store';

interface SidePanelProps {
  isOpen?: boolean;
}

const SidePanel: React.FC<SidePanelProps> = ({ isOpen }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(isOpen || false);

  const {
    conversations,
    currentConversationId,
    clearCurrentConversation,
    setCurrentConversation,
  } = useStore();

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  const handleNewConversation = () => {
    clearCurrentConversation();
    setIsSidebarOpen(false);
  };

  const handleSelectConversation = (id: string) => {
    setCurrentConversation(id);
    setIsSidebarOpen(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <>
      {/* Mobile menu button */}
      <button
        className="md:hidden fixed top-4 left-4 z-20 p-2 rounded-md bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-200"
        onClick={toggleSidebar}
      >
        {isSidebarOpen ? <FiX /> : <FiMenu />}
      </button>

      {/* Sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-10 w-64 bg-white dark:bg-gray-900 transform transition-transform duration-300 ease-in-out shadow-lg ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        <div className="flex flex-col h-full p-4">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold">Conversations</h2>
            <button
              onClick={toggleSidebar}
              className="md:hidden p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
            >
              <FiX />
            </button>
          </div>

          <button
            onClick={handleNewConversation}
            className="flex items-center justify-center space-x-2 p-2 mb-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            <FiPlusCircle />
            <span>New Flight</span>
          </button>

          <div className="overflow-y-auto flex-1 space-y-2">
            {conversations.map((conversation) => (
              <button
                key={conversation.id}
                onClick={() => handleSelectConversation(conversation.id)}
                className={`w-full text-left p-3 rounded-lg transition-colors flex items-start ${
                  currentConversationId === conversation.id
                    ? 'bg-gray-200 dark:bg-gray-700'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                <FiMessageSquare className="mt-1 mr-3 flex-shrink-0" />
                <div className="overflow-hidden">
                  <p className="font-medium truncate">{conversation.title}</p>
                  {conversation.createdAt && (
                    <p className="text-xs text-gray-500 truncate">
                      {formatDate(conversation.createdAt)}
                    </p>
                  )}
                </div>
              </button>
            ))}

            {conversations.length === 0 && (
              <p className="text-center text-gray-500 mt-4">
                No conversations yet. Start by entering flight details.
              </p>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default SidePanel;
