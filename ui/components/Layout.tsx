import React, { ReactNode } from 'react';
import { FiAirplay, FiSettings, FiBell, FiUser, FiMenu } from 'react-icons/fi';

interface LayoutProps {
  children: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <button
                type="button"
                className="md:hidden p-2 rounded-md text-gray-500 hover:text-gray-600 hover:bg-gray-100 focus:outline-none"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              >
                <FiMenu className="h-6 w-6" />
              </button>
              <div className="flex-shrink-0 flex items-center">
                <FiAirplay className="h-8 w-8 text-blue-600" />
                <span className="ml-2 text-xl font-bold text-gray-800">FlightAssist</span>
              </div>
              <nav className="hidden md:ml-6 md:flex md:space-x-8">
                <a href="#" className="border-blue-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Dashboard
                </a>
                <a href="#" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Flights
                </a>
                <a href="#" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                  Notifications
                </a>
              </nav>
            </div>
            <div className="flex items-center">
              <button className="p-2 rounded-full bg-gray-100 text-gray-500 hover:text-gray-600 hover:bg-gray-200 focus:outline-none">
                <FiBell className="h-5 w-5" />
              </button>
              <button className="ml-3 p-2 rounded-full bg-gray-100 text-gray-500 hover:text-gray-600 hover:bg-gray-200 focus:outline-none">
                <FiSettings className="h-5 w-5" />
              </button>
              <div className="ml-3 relative">
                <div>
                  <button className="max-w-xs bg-blue-600 rounded-full flex items-center text-sm focus:outline-none p-1">
                    <FiUser className="h-6 w-6 text-white" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Content Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Main Content */}
        <main className="flex-1 overflow-auto bg-gray-50 p-4 md:p-6">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
