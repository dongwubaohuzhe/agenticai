import React from 'react';
import { FiArrowRight, FiCalendar, FiClock, FiAirplay, FiMapPin, FiAlertCircle, FiCheck, FiX } from 'react-icons/fi';
import ChatInterface from './ChatInterface';

interface FlightDetailProps {
  flight: {
    number: string;
    origin: string;
    destination: string;
    date?: string;
    airline?: string;
    scheduled_departure?: string;
    status?: string;
  };
  onBack: () => void;
}

const FlightDetail: React.FC<FlightDetailProps> = ({ flight, onBack }) => {

  const airportNames: Record<string, string> = {
    'SFO': 'San Francisco International',
    'LAX': 'Los Angeles International',
    'JFK': 'John F. Kennedy International',
    'ORD': 'O\'Hare International',
    'DFW': 'Dallas/Fort Worth International',
    'SEA': 'Seattle-Tacoma International',
  };

  const airlineNames: Record<string, string> = {
    'UA': 'United Airlines',
    'DL': 'Delta Air Lines',
    'AA': 'American Airlines',
  };

  // Extract airline code from flight number
  const airlineCode = flight.number?.split(' ')[0] || '';
  const airlineName = flight.airline || airlineNames[airlineCode] || airlineCode;

  // Format flight info for the chat interface
  const flightInfo = {
    flightNumber: flight.number,
    origin: flight.origin,
    destination: flight.destination,
    airline: airlineName,
    date: flight.date || new Date().toISOString().split('T')[0],
    departureTime: flight.scheduled_departure || '08:00',
    status: flight.status || 'Scheduled'
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          Back to Dashboard
        </button>
        <div className="flex space-x-4">
          <button className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            <FiCheck className="mr-2 -ml-1 h-5 w-5 text-gray-400" />
            Save
          </button>
          <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Share Flight
          </button>
        </div>
      </div>

      {/* Flight Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between">
          <div>
            <div className="flex items-center">
              <FiAirplay className="h-6 w-6 text-blue-600 mr-2" />
              <h2 className="text-xl font-bold text-gray-900">Flight {flight.number}</h2>
              <span className={`ml-4 px-2.5 py-0.5 rounded-full text-xs font-medium
                ${flight.status === 'Delayed' ? 'bg-red-100 text-red-800' :
                  flight.status === 'On Time' ? 'bg-green-100 text-green-800' :
                  'bg-blue-100 text-blue-800'}`}>
                {flight.status || 'Scheduled'}
              </span>
            </div>
            <p className="mt-1 text-sm text-gray-500">{airlineName}</p>
          </div>
          <div className="mt-4 md:mt-0 flex items-center text-sm text-gray-500">
            <FiCalendar className="mr-1.5 h-5 w-5 text-gray-400" />
            <span>{flight.date || 'Today'}</span>
            {flight.scheduled_departure && (
              <>
                <FiClock className="ml-4 mr-1.5 h-5 w-5 text-gray-400" />
                <span>{flight.scheduled_departure}</span>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Flight Route */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Flight Route</h3>
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between">
          <div className="flex-1">
            <div className="flex flex-col items-center">
              <div className="bg-blue-100 p-3 rounded-full">
                <FiMapPin className="h-6 w-6 text-blue-700" />
              </div>
              <p className="mt-2 text-lg font-medium text-gray-900">{flight.origin}</p>
              <p className="text-sm text-gray-500">{airportNames[flight.origin] || flight.origin}</p>
            </div>
          </div>

          <div className="hidden md:block flex-1 px-4">
            <div className="flex items-center justify-center">
              <div className="w-full h-0.5 bg-gray-200"></div>
              <FiArrowRight className="mx-4 h-6 w-6 text-gray-400" />
              <div className="w-full h-0.5 bg-gray-200"></div>
            </div>
          </div>

          <div className="flex-1 mt-6 md:mt-0">
            <div className="flex flex-col items-center">
              <div className="bg-purple-100 p-3 rounded-full">
                <FiMapPin className="h-6 w-6 text-purple-700" />
              </div>
              <p className="mt-2 text-lg font-medium text-gray-900">{flight.destination}</p>
              <p className="text-sm text-gray-500">{airportNames[flight.destination] || flight.destination}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Flight Assistant */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white shadow rounded-lg overflow-hidden h-full">
            <div className="px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
              <h3 className="text-lg font-medium text-gray-900">Flight Assistant</h3>
              <p className="text-sm text-gray-500">Get real-time assistance for your flight</p>
            </div>
            <div className="h-[500px]">
              <ChatInterface flightInfo={flightInfo} />
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {/* Actions Card */}
          <div className="bg-white shadow rounded-lg p-5">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
            <div className="space-y-3">
              <button className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-md text-sm font-medium text-gray-700">
                Check Weather Information
                <FiArrowRight className="h-4 w-4 text-gray-400" />
              </button>
              <button className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-md text-sm font-medium text-gray-700">
                Find Alternative Flights
                <FiArrowRight className="h-4 w-4 text-gray-400" />
              </button>
              <button className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-md text-sm font-medium text-gray-700">
                Manage Hotel Reservations
                <FiArrowRight className="h-4 w-4 text-gray-400" />
              </button>
              <button className="w-full flex items-center justify-between px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-md text-sm font-medium text-gray-700">
                Notify Contacts
                <FiArrowRight className="h-4 w-4 text-gray-400" />
              </button>
            </div>
          </div>

          {/* Delay Alert */}
          {flight.status === 'Delayed' && (
            <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-md">
              <div className="flex">
                <div className="flex-shrink-0">
                  <FiAlertCircle className="h-5 w-5 text-red-400" />
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Flight Delayed</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>Your flight has been delayed. Our assistant can help you check for alternative travel options.</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FlightDetail;
