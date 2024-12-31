# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Install node and npm
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the Python requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json and package-lock.json (if they exist)
# COPY package*.json ./

# Install Node.js dependencies
# RUN npm install

# Copy the rest of your application's code
COPY . .

EXPOSE 8501

# Command to run Streamlit
CMD ["streamlit", "run", "app.py"]