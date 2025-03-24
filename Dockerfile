FROM python:3.9-slim as base

# Set working directory
WORKDIR /app

# Install Node.js for the frontend
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy Python requirements and install dependencies
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir .[dev]

# Copy source code
COPY src/ ./src/
COPY ui/ ./ui/

# Build the frontend
WORKDIR /app/ui
RUN npm install
RUN npm run build

# Set back to main directory
WORKDIR /app

# Expose ports for API and UI
EXPOSE 8000
EXPOSE 3000

# Command to run both API and UI
CMD ["python", "-m", "agenticai.run_app"]
