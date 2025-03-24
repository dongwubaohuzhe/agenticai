import React, { useState } from 'react';

export default function BasicPage() {
  const [flightInfo, setFlightInfo] = useState({
    flight_number: '',
    origin: '',
    destination: '',
    scheduled_departure: ''
  });

  const [submitted, setSubmitted] = useState(false);
  const [questions, setQuestions] = useState<string[]>([]);
  const [responses, setResponses] = useState<string[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFlightInfo(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  const handleQuestionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentQuestion.trim()) return;

    setQuestions([...questions, currentQuestion]);

    // Generate a simple response
    let response = `I'll check about ${currentQuestion} for your flight ${flightInfo.flight_number}.`;
    if (currentQuestion.toLowerCase().includes('delay')) {
      response = `Your flight ${flightInfo.flight_number} is currently on time. No delays are expected.`;
    } else if (currentQuestion.toLowerCase().includes('weather')) {
      response = `The weather at ${flightInfo.destination} is clear with a temperature of 75°F.`;
    }

    setResponses([...responses, response]);
    setCurrentQuestion('');
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>Flight Assistance</h1>

      {!submitted ? (
        <div>
          <h2>Enter Flight Details</h2>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            <div>
              <label htmlFor="flight_number">Flight Number: </label>
              <input
                type="text"
                id="flight_number"
                name="flight_number"
                value={flightInfo.flight_number}
                onChange={handleChange}
                required
                style={{ padding: '8px', marginLeft: '10px' }}
              />
            </div>

            <div>
              <label htmlFor="origin">Origin: </label>
              <input
                type="text"
                id="origin"
                name="origin"
                value={flightInfo.origin}
                onChange={handleChange}
                required
                style={{ padding: '8px', marginLeft: '10px' }}
              />
            </div>

            <div>
              <label htmlFor="destination">Destination: </label>
              <input
                type="text"
                id="destination"
                name="destination"
                value={flightInfo.destination}
                onChange={handleChange}
                required
                style={{ padding: '8px', marginLeft: '10px' }}
              />
            </div>

            <div>
              <label htmlFor="scheduled_departure">Departure Date: </label>
              <input
                type="date"
                id="scheduled_departure"
                name="scheduled_departure"
                value={flightInfo.scheduled_departure}
                onChange={handleChange}
                required
                style={{ padding: '8px', marginLeft: '10px' }}
              />
            </div>

            <button
              type="submit"
              style={{
                padding: '10px',
                backgroundColor: '#3B82F6',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
                marginTop: '10px'
              }}
            >
              Submit
            </button>
          </form>
        </div>
      ) : (
        <div>
          <h2>Flight Information</h2>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            background: '#f8fafc',
            padding: '15px',
            borderRadius: '8px',
            marginBottom: '20px'
          }}>
            <div>
              <p><strong>Flight:</strong> {flightInfo.flight_number}</p>
              <p><strong>Route:</strong> {flightInfo.origin} to {flightInfo.destination}</p>
            </div>
            <div>
              <p><strong>Date:</strong> {flightInfo.scheduled_departure}</p>
              <p><strong>Status:</strong> On Time</p>
            </div>
          </div>

          <h3>Ask About Your Flight</h3>
          <form onSubmit={handleQuestionSubmit} style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
            <input
              type="text"
              value={currentQuestion}
              onChange={(e) => setCurrentQuestion(e.target.value)}
              placeholder="Ask a question..."
              style={{ flex: 1, padding: '10px', borderRadius: '5px', border: '1px solid #e2e8f0' }}
            />
            <button
              type="submit"
              style={{
                padding: '10px 15px',
                backgroundColor: '#3B82F6',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer'
              }}
            >
              Ask
            </button>
          </form>

          <div>
            {questions.map((question, index) => (
              <div key={index} style={{ marginBottom: '15px' }}>
                <div style={{
                  backgroundColor: '#3B82F6',
                  color: 'white',
                  padding: '10px',
                  borderRadius: '8px',
                  borderTopRightRadius: '0',
                  alignSelf: 'flex-end',
                  marginLeft: 'auto',
                  maxWidth: '80%',
                  display: 'inline-block'
                }}>
                  {question}
                </div>
                <div style={{ clear: 'both', height: '10px' }}></div>
                <div style={{
                  backgroundColor: '#f1f5f9',
                  padding: '10px',
                  borderRadius: '8px',
                  borderTopLeftRadius: '0',
                  maxWidth: '80%',
                  display: 'inline-block'
                }}>
                  {responses[index]}
                </div>
              </div>
            ))}
          </div>

          <div style={{ marginTop: '20px' }}>
            <h3>Suggested Questions</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <button
                onClick={() => setCurrentQuestion('Is my flight delayed?')}
                style={{
                  textAlign: 'left',
                  padding: '8px',
                  background: '#f1f5f9',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer'
                }}
              >
                Is my flight delayed?
              </button>
              <button
                onClick={() => setCurrentQuestion('What is the weather at my destination?')}
                style={{
                  textAlign: 'left',
                  padding: '8px',
                  background: '#f1f5f9',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer'
                }}
              >
                What is the weather at my destination?
              </button>
              <button
                onClick={() => setCurrentQuestion('When should I arrive at the airport?')}
                style={{
                  textAlign: 'left',
                  padding: '8px',
                  background: '#f1f5f9',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer'
                }}
              >
                When should I arrive at the airport?
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
