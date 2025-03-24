import React, { useState, useEffect } from 'react';

export default function BasicPage() {
  const [flightInfo, setFlightInfo] = useState({
    flight_number: '',
    origin: '',
    destination: '',
    scheduled_departure: '',
    disruption: 'None'
  });

  const [submitted, setSubmitted] = useState(false);
  const [questions, setQuestions] = useState<string[]>([]);
  const [responses, setResponses] = useState<string[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [originSuggestions, setOriginSuggestions] = useState<Array<{code: string, name: string}>>([]);
  const [destinationSuggestions, setDestinationSuggestions] = useState<Array<{code: string, name: string}>>([]);
  const [showOriginSuggestions, setShowOriginSuggestions] = useState(false);
  const [showDestinationSuggestions, setShowDestinationSuggestions] = useState(false);
  
  // Animation states
  const [fadeIn, setFadeIn] = useState(false);
  
  // Disruption options
  const disruptionTypes = [
    { value: 'None', label: 'No Disruption' },
    { value: 'Weather', label: 'Bad Weather' },
    { value: 'Technical', label: 'Technical Issue' },
    { value: 'Congestion', label: 'Airport Congestion' },
    { value: 'Staffing', label: 'Crew Shortage' }
  ];

  // Airport data for autofill
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
  ];
  
  useEffect(() => {
    setFadeIn(true);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFlightInfo(prev => ({ ...prev, [name]: value }));
    
    // Filter airport suggestions based on input
    if (name === 'origin') {
      const filtered = airports.filter(
        airport => airport.code.toLowerCase().includes(value.toLowerCase()) || 
                  airport.name.toLowerCase().includes(value.toLowerCase())
      );
      setOriginSuggestions(filtered);
      setShowOriginSuggestions(value.length > 0 && filtered.length > 0);
    } else if (name === 'destination') {
      const filtered = airports.filter(
        airport => airport.code.toLowerCase().includes(value.toLowerCase()) || 
                  airport.name.toLowerCase().includes(value.toLowerCase())
      );
      setDestinationSuggestions(filtered);
      setShowDestinationSuggestions(value.length > 0 && filtered.length > 0);
    }
  };

  const selectAirport = (type: 'origin' | 'destination', airport: { code: string, name: string }) => {
    setFlightInfo(prev => ({ ...prev, [type]: airport.code }));
    if (type === 'origin') {
      setShowOriginSuggestions(false);
    } else {
      setShowDestinationSuggestions(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  const getFlightStatus = () => {
    // Return status based on disruption
    switch(flightInfo.disruption) {
      case 'Weather':
        return 'Delayed';
      case 'Technical':
        return 'Delayed';
      case 'Congestion':
        return 'Delayed';
      case 'Staffing':
        return 'Cancelled';
      default:
        return 'On Time';
    }
  };

  const getWeatherInfo = () => {
    // Return weather based on disruption
    if (flightInfo.disruption === 'Weather') {
      return 'Severe thunderstorms, 45°F';
    } 
    return 'Clear, 75°F';
  };

  const handleQuestionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQuestion.trim()) return;

    setQuestions([...questions, currentQuestion]);

    // Generate response based on disruption and question
    let response = `I'll check about ${currentQuestion} for your flight ${flightInfo.flight_number}.`;
    
    if (currentQuestion.toLowerCase().includes('delay')) {
      if (flightInfo.disruption !== 'None') {
        response = `Your flight ${flightInfo.flight_number} is currently ${getFlightStatus().toLowerCase()} due to ${flightInfo.disruption.toLowerCase()} issues.`;
        
        if (flightInfo.disruption === 'Weather') {
          response += ' We expect a delay of approximately 2 hours.';
        } else if (flightInfo.disruption === 'Technical') {
          response += ' Engineers are working on the issue. We expect a delay of approximately 1.5 hours.';
        } else if (flightInfo.disruption === 'Congestion') {
          response += ' Air traffic control is managing the situation. We expect a delay of approximately 1 hour.';
        } else if (flightInfo.disruption === 'Staffing') {
          response += ' Unfortunately, we had to cancel this flight due to crew shortage. Our agents will help you book an alternative flight.';
        }
      } else {
        response = `Your flight ${flightInfo.flight_number} is currently on time. No delays are expected.`;
      }
    } else if (currentQuestion.toLowerCase().includes('weather')) {
      response = `The weather at ${flightInfo.destination} is ${getWeatherInfo()}.`;
      
      if (flightInfo.disruption === 'Weather') {
        response += ' These conditions are causing significant delays across the network.';
      }
    } else if (currentQuestion.toLowerCase().includes('alternative') || currentQuestion.toLowerCase().includes('other flight')) {
      if (flightInfo.disruption !== 'None') {
        response = `I can help you find alternative flights from ${flightInfo.origin} to ${flightInfo.destination}. There's a flight available tomorrow morning at 8:00 AM.`;
      } else {
        response = `Your current flight is on schedule. If you'd still like to change your flight, I can help you find alternatives.`;
      }
    }

    setResponses([...responses, response]);
    setCurrentQuestion('');
  };

  return (
    <div className={`max-w-4xl mx-auto p-6 transition-opacity duration-500 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}>
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-blue-600 mb-2">Flight Assistant Pro</h1>
        <p className="text-gray-600">Your intelligent travel companion</p>
      </div>

      {!submitted ? (
        <div className="bg-white rounded-xl shadow-lg p-8 transition-all duration-300 hover:shadow-xl">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
            <span className="mr-2 text-blue-500">✈️</span>
            Enter Flight Details
          </h2>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="relative">
              <label htmlFor="flight_number" className="block text-sm font-medium text-gray-700 mb-1">Flight Number</label>
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-400">✈️</span>
                </div>
                <input
                  type="text"
                  id="flight_number"
                  name="flight_number"
                  value={flightInfo.flight_number}
                  onChange={handleChange}
                  required
                  className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border border-gray-300 rounded-md py-3"
                  placeholder="AA1234"
                />
              </div>
            </div>

            <div className="relative">
              <label htmlFor="origin" className="block text-sm font-medium text-gray-700 mb-1">Origin</label>
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-400">📍</span>
                </div>
                <input
                  type="text"
                  id="origin"
                  name="origin"
                  value={flightInfo.origin}
                  onChange={handleChange}
                  required
                  className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border border-gray-300 rounded-md py-3"
                  placeholder="Airport code or name"
                  autoComplete="off"
                />
              </div>
              {showOriginSuggestions && (
                <div className="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md py-1 text-sm">
                  {originSuggestions.map((airport) => (
                    <div 
                      key={airport.code}
                      className="px-4 py-2 hover:bg-blue-100 cursor-pointer flex justify-between"
                      onClick={() => selectAirport('origin', airport)}
                    >
                      <span>{airport.name}</span>
                      <span className="text-gray-500">{airport.code}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="relative">
              <label htmlFor="destination" className="block text-sm font-medium text-gray-700 mb-1">Destination</label>
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-400">📍</span>
                </div>
                <input
                  type="text"
                  id="destination"
                  name="destination"
                  value={flightInfo.destination}
                  onChange={handleChange}
                  required
                  className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border border-gray-300 rounded-md py-3"
                  placeholder="Airport code or name"
                  autoComplete="off"
                />
              </div>
              {showDestinationSuggestions && (
                <div className="absolute z-10 mt-1 w-full bg-white shadow-lg rounded-md py-1 text-sm">
                  {destinationSuggestions.map((airport) => (
                    <div 
                      key={airport.code}
                      className="px-4 py-2 hover:bg-blue-100 cursor-pointer flex justify-between"
                      onClick={() => selectAirport('destination', airport)}
                    >
                      <span>{airport.name}</span>
                      <span className="text-gray-500">{airport.code}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="relative">
              <label htmlFor="scheduled_departure" className="block text-sm font-medium text-gray-700 mb-1">Departure Date</label>
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-400">📅</span>
                </div>
                <input
                  type="date"
                  id="scheduled_departure"
                  name="scheduled_departure"
                  value={flightInfo.scheduled_departure}
                  onChange={handleChange}
                  required
                  className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border border-gray-300 rounded-md py-3"
                />
              </div>
            </div>

            <div className="relative">
              <label htmlFor="disruption" className="block text-sm font-medium text-gray-700 mb-1">Flight Disruption Simulation</label>
              <div className="relative rounded-md shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-400">⚠️</span>
                </div>
                <select
                  id="disruption"
                  name="disruption"
                  value={flightInfo.disruption}
                  onChange={handleChange}
                  className="focus:ring-blue-500 focus:border-blue-500 block w-full pl-10 sm:text-sm border border-gray-300 rounded-md py-3"
                >
                  {disruptionTypes.map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              type="submit"
              className="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition duration-150 ease-in-out transform hover:scale-105"
            >
              Find Flight Information <span className="ml-2">→</span>
            </button>
          </form>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-lg p-8 transition-all duration-300 animate-fade-in">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
            <span className="mr-2 text-blue-500">✈️</span>
            Flight Information
          </h2>
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6 mb-8 shadow-inner">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <p className="text-gray-500 text-sm">Flight</p>
                <p className="text-lg font-bold">{flightInfo.flight_number}</p>
                
                <div className="flex items-center mt-4">
                  <div className="flex flex-col items-center">
                    <div className="bg-blue-100 rounded-full p-2">
                      <span className="text-blue-600">📍</span>
                    </div>
                    <div className="h-14 w-0.5 bg-gray-300 my-1"></div>
                    <div className="bg-indigo-100 rounded-full p-2">
                      <span className="text-indigo-600">📍</span>
                    </div>
                  </div>
                  <div className="ml-4">
                    <div className="mb-4">
                      <p className="text-sm text-gray-500">Origin</p>
                      <p className="font-bold">{flightInfo.origin}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Destination</p>
                      <p className="font-bold">{flightInfo.destination}</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div>
                <p className="text-gray-500 text-sm">Departure Date</p>
                <p className="text-lg font-bold">{flightInfo.scheduled_departure}</p>
                
                <div className="mt-4">
                  <p className="text-gray-500 text-sm">Status</p>
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                    getFlightStatus() === 'On Time' ? 'bg-green-100 text-green-800' : 
                    getFlightStatus() === 'Delayed' ? 'bg-yellow-100 text-yellow-800' : 
                    'bg-red-100 text-red-800'
                  } mt-1`}>
                    {getFlightStatus()}
                    {flightInfo.disruption !== 'None' && ` (${flightInfo.disruption})`}
                  </span>
                </div>
                
                <div className="mt-4">
                  <p className="text-gray-500 text-sm">Weather at Destination</p>
                  <p className="font-medium">{getWeatherInfo()}</p>
                </div>

                {flightInfo.disruption !== 'None' && (
                  <div className="mt-4 p-3 bg-amber-50 rounded-md border border-amber-200">
                    <p className="text-amber-800 font-medium flex items-center">
                      <span className="mr-2">⚠️</span>
                      Disruption Alert
                    </p>
                    <p className="text-sm text-amber-700 mt-1">
                      {flightInfo.disruption === 'Weather' && 'Severe weather conditions affecting this flight.'}
                      {flightInfo.disruption === 'Technical' && 'Technical issues affecting this aircraft.'}
                      {flightInfo.disruption === 'Congestion' && 'Airport congestion causing delays.'}
                      {flightInfo.disruption === 'Staffing' && 'Crew shortage has led to flight cancellation.'}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          <h3 className="text-xl font-semibold mb-4 flex items-center">
            <span className="mr-2 text-blue-500">💬</span>
            Ask About Your Flight
          </h3>
          <form onSubmit={handleQuestionSubmit} className="mb-6">
            <div className="flex rounded-md shadow-sm">
              <input
                type="text"
                value={currentQuestion}
                onChange={(e) => setCurrentQuestion(e.target.value)}
                placeholder="Ask a question..."
                className="flex-1 min-w-0 block w-full px-4 py-3 rounded-none rounded-l-md sm:text-sm border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
              />
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-r-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Ask
              </button>
            </div>
          </form>

          <div className="space-y-4 mb-8 max-h-96 overflow-y-auto p-4 bg-gray-50 rounded-lg">
            {questions.length === 0 ? (
              <p className="text-center text-gray-500 py-8">Ask a question to get started</p>
            ) : (
              questions.map((question, index) => (
                <div key={index} className="animate-fade-in">
                  <div className="bg-blue-600 text-white p-3 rounded-lg rounded-br-none max-w-[80%] ml-auto">
                    {question}
                  </div>
                  <div className="mt-2 bg-white p-3 rounded-lg rounded-bl-none shadow-sm border border-gray-200 max-w-[80%]">
                    {responses[index]}
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-lg font-medium mb-3">Suggested Questions</h3>
            <div className="grid gap-2">
              <button
                onClick={() => setCurrentQuestion('Is my flight delayed?')}
                className="text-left p-3 bg-white rounded-md border border-gray-200 hover:bg-blue-50 transition duration-150 shadow-sm hover:shadow"
              >
                Is my flight delayed?
              </button>
              <button
                onClick={() => setCurrentQuestion('What is the weather at my destination?')}
                className="text-left p-3 bg-white rounded-md border border-gray-200 hover:bg-blue-50 transition duration-150 shadow-sm hover:shadow"
              >
                What is the weather at my destination?
              </button>
              <button
                onClick={() => setCurrentQuestion('Are there alternative flights available?')}
                className="text-left p-3 bg-white rounded-md border border-gray-200 hover:bg-blue-50 transition duration-150 shadow-sm hover:shadow"
              >
                Are there alternative flights available?
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
