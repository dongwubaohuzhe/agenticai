'use client';

import React, { useState } from 'react';
import { FiArrowRight, FiCalendar, FiClock, FiMapPin, FiPlane } from 'react-icons/fi';
import { useStore } from '../lib/store';
import { FlightInfo } from '../lib/api';

interface FlightFormProps {
  onSubmit?: (data: FlightInfo) => void;
}

const FlightForm: React.FC<FlightFormProps> = ({ onSubmit }) => {
  const { createConversation } = useStore();
  const [step, setStep] = useState<1 | 2>(1);
  const [flightInfo, setFlightInfo] = useState<FlightInfo>({
    flight_number: '',
    origin: '',
    destination: '',
    scheduled_departure: '',
    airline: '',
  });

  // Mock data for dropdowns
  const airlines = [
    'American Airlines',
    'Delta Air Lines',
    'United Airlines',
    'Southwest Airlines',
    'JetBlue Airways',
    'Alaska Airlines',
    'Air Canada',
    'British Airways',
    'Lufthansa',
    'Emirates',
  ];

  const airports = [
    { code: 'ATL', name: 'Atlanta Hartsfield-Jackson' },
    { code: 'LAX', name: 'Los Angeles International' },
    { code: 'ORD', name: 'Chicago O\'Hare' },
    { code: 'DFW', name: 'Dallas/Fort Worth' },
    { code: 'DEN', name: 'Denver International' },
    { code: 'JFK', name: 'New York Kennedy' },
    { code: 'SFO', name: 'San Francisco International' },
    { code: 'SEA', name: 'Seattle-Tacoma' },
    { code: 'LAS', name: 'Las Vegas McCarran' },
    { code: 'MCO', name: 'Orlando International' },
    { code: 'MIA', name: 'Miami International' },
    { code: 'CLT', name: 'Charlotte Douglas' },
    { code: 'EWR', name: 'Newark Liberty' },
    { code: 'PHX', name: 'Phoenix Sky Harbor' },
    { code: 'IAH', name: 'Houston George Bush' },
    { code: 'BOS', name: 'Boston Logan' },
    { code: 'LHR', name: 'London Heathrow' },
    { code: 'CDG', name: 'Paris Charles de Gaulle' },
    { code: 'FRA', name: 'Frankfurt Airport' },
    { code: 'AMS', name: 'Amsterdam Schiphol' },
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFlightInfo(prev => ({ ...prev, [name]: value }));
  };

  const handleNextStep = (e: React.FormEvent) => {
    e.preventDefault();
    setStep(2);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Format date and time into ISO string
    const departureDate = flightInfo.scheduled_departure;

    // Create a properly formatted flight info object
    const formattedFlightInfo: FlightInfo = {
      ...flightInfo,
      scheduled_departure: departureDate,
    };

    // Start a new conversation with this flight data
    createConversation(formattedFlightInfo);

    // Call the onSubmit prop if it exists
    if (onSubmit) {
      onSubmit(formattedFlightInfo);
    }
  };

  return (
    <div className="max-w-2xl mx-auto w-full bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-center mb-6">Flight Information</h2>

      {step === 1 ? (
        <form onSubmit={handleNextStep} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">
              Flight Number <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <FiPlane className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                name="flight_number"
                value={flightInfo.flight_number}
                onChange={handleChange}
                placeholder="AA1234"
                className="w-full pl-10 p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Origin <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <FiMapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <select
                name="origin"
                value={flightInfo.origin}
                onChange={handleChange}
                className="w-full pl-10 p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select Origin Airport</option>
                {airports.map(airport => (
                  <option key={airport.code} value={airport.code}>
                    {airport.code} - {airport.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Destination <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <FiMapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <select
                name="destination"
                value={flightInfo.destination}
                onChange={handleChange}
                className="w-full pl-10 p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              >
                <option value="">Select Destination Airport</option>
                {airports.map(airport => (
                  <option key={airport.code} value={airport.code}>
                    {airport.code} - {airport.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
            >
              Next <FiArrowRight className="inline ml-1" />
            </button>
          </div>
        </form>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">
              Airline
            </label>
            <div className="relative">
              <FiPlane className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <select
                name="airline"
                value={flightInfo.airline}
                onChange={handleChange}
                className="w-full pl-10 p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select Airline</option>
                {airlines.map(airline => (
                  <option key={airline} value={airline}>
                    {airline}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Departure Date <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <FiCalendar className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="date"
                name="scheduled_departure"
                value={flightInfo.scheduled_departure}
                onChange={handleChange}
                className="w-full pl-10 p-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
          </div>

          <div className="flex space-x-4">
            <button
              type="button"
              onClick={() => setStep(1)}
              className="flex-1 border border-gray-300 text-gray-700 dark:text-gray-200 py-2 px-4 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            >
              Back
            </button>
            <button
              type="submit"
              className="flex-1 bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition-colors"
            >
              Start
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default FlightForm;
