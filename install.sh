#!/bin/bash

echo "🔧 Setting up GitEcho..."

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 could not be found. Please install Python 3.7+."
    exit
fi

# Set up virtual environment
python3 -m venv venv
if [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
else
  . venv/bin/activate
fi

# Install dependencies
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "📄 .env file created. Please update it with your OpenAI API key."
fi

echo "✅ GitEcho is ready. You can now run: python gitecho.py"
