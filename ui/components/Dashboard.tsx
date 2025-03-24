import React from 'react';
import { FiCloud, FiWind, FiClock, FiMapPin, FiThermometer, FiAlertCircle, FiCheckCircle, FiCalendar } from 'react-icons/fi';
import FlightForm from './FlightForm';

interface DashboardProps {
  onSelectFlight: (flightData: any) => void;
}

const Dashboard: React.FC<DashboardProps> = ({ onSelectFlight }) => {

  const recentFlights = [
    { id: 1, number: 'UA 354', origin: 'SFO', destination: 'ORD', date: '2023-10-30', status: 'On Time' },
    { id: 2, number: 'DL 1242', origin: 'LAX', destination: 'JFK', date: '2023-10-28', status: 'Delayed' },
    { id: 3, number: 'AA 789', origin: 'SEA', destination: 'DFW', date: '2023-10-25', status: 'Completed' },
  ];

  const weatherData = {
    origin: { location: 'San Francisco', condition: 'Cloudy', temp: 58, wind: 12 },
    destination: { location: 'Chicago', condition: 'Rainy', temp: 48, wind: 15 }
  };

  const handleFlightSubmit = (data: any) => {
    // Process the flight data
    onSelectFlight({
      ...data,
      status: 'Scheduled'
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row gap-4 md:items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Flight Delay Dashboard</h1>
        <div className="flex items-center text-sm text-gray-500">
          <FiCalendar className="mr-1.5 h-5 w-5 text-gray-400" />
          <span>{new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</span>
        </div>
      </div>

      {/* Flight Entry Card */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">Track Your Flight</h2>
        <FlightForm onSubmit={handleFlightSubmit} />
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Weather Origin Card */}
        <div className="bg-white shadow rounded-lg p-5 border-l-4 border-blue-500">
          <div className="flex justify-between">
            <div className="flex items-center">
              <FiMapPin className="h-5 w-5 text-blue-500 mr-2" />
              <h3 className="text-sm font-medium text-gray-700">Weather at Origin</h3>
            </div>
            <FiCloud className="h-8 w-8 text-blue-400" />
          </div>
          <div className="mt-4">
            <p className="text-xl font-semibold">{weatherData.origin.location}</p>
            <div className="flex justify-between items-center mt-2">
              <div className="flex items-center">
                <FiThermometer className="h-4 w-4 text-gray-500 mr-1" />
                <span className="text-sm text-gray-600">{weatherData.origin.temp}°F</span>
              </div>
              <div className="flex items-center">
                <FiWind className="h-4 w-4 text-gray-500 mr-1" />
                <span className="text-sm text-gray-600">{weatherData.origin.wind} mph</span>
              </div>
              <span className="text-sm text-gray-600">{weatherData.origin.condition}</span>
            </div>
          </div>
        </div>

        {/* Weather Destination Card */}
        <div className="bg-white shadow rounded-lg p-5 border-l-4 border-purple-500">
          <div className="flex justify-between">
            <div className="flex items-center">
              <FiMapPin className="h-5 w-5 text-purple-500 mr-2" />
              <h3 className="text-sm font-medium text-gray-700">Weather at Destination</h3>
            </div>
            <FiCloud className="h-8 w-8 text-purple-400" />
          </div>
          <div className="mt-4">
            <p className="text-xl font-semibold">{weatherData.destination.location}</p>
            <div className="flex justify-between items-center mt-2">
              <div className="flex items-center">
                <FiThermometer className="h-4 w-4 text-gray-500 mr-1" />
                <span className="text-sm text-gray-600">{weatherData.destination.temp}°F</span>
              </div>
              <div className="flex items-center">
                <FiWind className="h-4 w-4 text-gray-500 mr-1" />
                <span className="text-sm text-gray-600">{weatherData.destination.wind} mph</span>
              </div>
              <span className="text-sm text-gray-600">{weatherData.destination.condition}</span>
            </div>
          </div>
        </div>

        {/* Delay Risk Card */}
        <div className="bg-white shadow rounded-lg p-5 border-l-4 border-amber-500">
          <div className="flex justify-between">
            <div className="flex items-center">
              <FiClock className="h-5 w-5 text-amber-500 mr-2" />
              <h3 className="text-sm font-medium text-gray-700">Delay Risk Analysis</h3>
            </div>
            <FiAlertCircle className="h-8 w-8 text-amber-400" />
          </div>
          <div className="mt-4">
            <p className="text-xl font-semibold">Medium Risk</p>
            <p className="text-sm text-gray-600 mt-2">Weather conditions at your destination may cause minor delays. Plan accordingly.</p>
          </div>
        </div>
      </div>

      {/* Recent Flights Table */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Recent Flights</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Flight</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Route</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {recentFlights.map((flight) => (
                <tr key={flight.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{flight.number}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{flight.origin} → {flight.destination}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{flight.date}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full
                      ${flight.status === 'On Time' ? 'bg-green-100 text-green-800' :
                        flight.status === 'Delayed' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'}`}>
                      {flight.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button
                      onClick={() => onSelectFlight(flight)}
                      className="text-blue-600 hover:text-blue-900">
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
