#!/bin/bash

# Exit on error
set -e

echo "Setting up Flight Delay Response System development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
  echo "Creating Python virtual environment..."
  python -m venv .venv

  if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
  else
    source .venv/Scripts/activate
  fi
else
  echo "Virtual environment already exists, activating..."
  if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
  else
    source .venv/Scripts/activate
  fi
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -e .

# Install Node.js dependencies for the UI
echo "Installing UI dependencies..."
cd ui
npm install
cd ..

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p data
mkdir -p logs

# Setup complete
echo ""
echo "Setup complete! 🚀"
echo ""
echo "To start the application:"
echo "  1. Activate the virtual environment: source .venv/bin/activate (Linux/Mac) or .venv\\Scripts\\activate (Windows)"
echo "  2. Run the full application: python -m agenticai.run_app"
echo ""
echo "Or run the components separately:"
echo "  - API only: python -m agenticai.run_api"
echo "  - UI only: cd ui && npm run dev"
echo ""
