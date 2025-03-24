# Flight Delay Response System

A multi-agent system built with CrewAI for handling flight delays intelligently.

This system monitors flights, analyzes delay risks based on weather and other factors, suggests alternative routes, adjusts reservations, notifies stakeholders, and organizes travel documents.

## Features

- **Weather Analysis**: Real-time weather monitoring for departure and arrival airports
- **Flight Delay Detection**: Advanced prediction of flight delays with reason analysis
- **Reservation Management**: Automatic adjustments to hotel and car rental reservations
- **Stakeholder Notifications**: Keep family, colleagues, and business contacts updated
- **Alternative Routes**: Intelligent suggestions for backup travel options
- **Travel Organization**: Document management for changing itineraries

## Architecture

The system uses a multi-agent approach, where specialized agents collaborate to handle different aspects of flight delays:

- `WeatherCheckerAgent`: Monitors weather conditions that might affect flights
- `FlightDelayScannerAgent`: Detects and predicts potential flight delays
- `ReservationAdjusterAgent`: Updates hotel and rental car bookings
- `StakeholderNotifierAgent`: Communicates changes to relevant contacts
- `AlternativeRouteSuggesterAgent`: Recommends backup travel options
- `TravelOrganizerAgent`: Manages travel documents and itineraries

## Components

The system consists of:

1. **Python Backend**: A FastAPI application that powers the multi-agent system
2. **Next.js Frontend**: A modern UI for interacting with the system
3. **Agent Framework**: Built with CrewAI for agent collaboration
4. **Memory System**: ChromaDB for maintaining conversation history
5. **Monitoring**: Arize Phoenix for tracking agent performance

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+ and npm
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/flight-delay-system.git
cd flight-delay-system
```

2. Install Python dependencies:

```bash
pip install -e .
```

3. Install UI dependencies:

```bash
cd ui
npm install
```

### Running the Application

#### Development Mode

To start both the API and UI in development mode:

```bash
python -m agenticai.run_app
```

Or start them separately:

- Backend API only:

```bash
python -m agenticai.run_api
```

- Frontend UI only:

```bash
cd ui
npm run dev
```

#### Production Deployment

Using Docker:

```bash
docker build -t flight-delay-system .
docker run -p 8000:8000 -p 3000:3000 flight-delay-system
```

## API Documentation

The API documentation is available at `http://localhost:8000/docs` when the server is running.

### Key Endpoints

- `POST /api/flight/status`: Check flight delay probability
- `GET /api/weather/{airport_code}`: Get weather information
- `POST /api/flight/alternatives`: Get alternative routes
- `POST /api/reservations/update`: Update reservations
- `POST /api/notifications/send`: Send notifications to stakeholders
- `POST /api/chat`: Process chat messages with the multi-agent system

## UI Features

The frontend provides:

- Flight information input
- Real-time chat interface
- Flight status monitoring
- Weather visualization
- Alternative route suggestions
- Reservation management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

# agenticai

[![Release](https://img.shields.io/github/v/release/dongwubaohuzhe/agenticai)](https://img.shields.io/github/v/release/dongwubaohuzhe/agenticai)
[![Build status](https://img.shields.io/github/actions/workflow/status/dongwubaohuzhe/agenticai/main.yml?branch=main)](https://github.com/dongwubaohuzhe/agenticai/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/dongwubaohuzhe/agenticai/branch/main/graph/badge.svg)](https://codecov.io/gh/dongwubaohuzhe/agenticai)
[![Commit activity](https://img.shields.io/github/commit-activity/m/dongwubaohuzhe/agenticai)](https://img.shields.io/github/commit-activity/m/dongwubaohuzhe/agenticai)
[![License](https://img.shields.io/github/license/dongwubaohuzhe/agenticai)](https://img.shields.io/github/license/dongwubaohuzhe/agenticai)

This is all about multi-agents

- **Github repository**: <https://github.com/dongwubaohuzhe/agenticai/>
- **Documentation** <https://dongwubaohuzhe.github.io/agenticai/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:dongwubaohuzhe/agenticai.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version

- Create an API Token on [PyPI](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/dongwubaohuzhe/agenticai/settings/secrets/actions/new).
- Create a [new release](https://github.com/dongwubaohuzhe/agenticai/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/cicd/#how-to-trigger-a-release).

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
