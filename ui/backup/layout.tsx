import '../styles/globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Flight Delay Response System',
  description: 'A multi-agent system for managing flight delays and travel disruptions',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen flex flex-col">
          <header className="bg-primary text-white p-4 shadow-md">
            <div className="max-w-7xl mx-auto">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    className="w-6 h-6"
                  >
                    <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
                  </svg>
                  <span className="font-bold text-xl">Flight Delay Response</span>
                </div>
                <nav className="hidden md:flex space-x-6">
                  <a href="#" className="hover:text-gray-200 transition-colors">Dashboard</a>
                  <a href="#" className="hover:text-gray-200 transition-colors">Documentation</a>
                  <a href="#" className="hover:text-gray-200 transition-colors">About</a>
                </nav>
              </div>
            </div>
          </header>

          <main className="flex-1">
            {children}
          </main>

          <footer className="bg-gray-100 dark:bg-gray-900 text-gray-600 dark:text-gray-400 p-4 text-center text-sm">
            <div className="max-w-7xl mx-auto">
              <p>© {new Date().getFullYear()} Flight Delay Response System. All rights reserved.</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
}
