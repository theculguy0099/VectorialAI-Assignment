#!/usr/bin/env python3
"""
Main startup script for the Multi-Agent Conversational AI system.
This script handles data processing, persona discovery, and starts the API server.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'langchain', 'langgraph', 'fastapi', 'uvicorn',
        'pandas', 'scikit-learn', 'sentence-transformers',
        'openai', 'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required dependencies are installed")
    return True

def check_data_files():
    """Check if required data files exist."""
    required_files = [
        'data/full_dialogues.csv',
        'data/dialogues_with_personas.csv',
        'data/persona_0_data.csv',
        'data/persona_1_data.csv',
        'data/persona_2_data.csv'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing data files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required data files exist")
    return True

def process_data():
    """Process the Cornell Movie-Dialogs Corpus data."""
    print("📊 Processing Cornell Movie-Dialogs Corpus data...")
    
    try:
        # Run data loader
        subprocess.run([sys.executable, "backend/data_loader.py"], check=True)
        print("✅ Data processing completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Data processing failed: {e}")
        return False

def discover_personas():
    """Run persona discovery process."""
    print("🔍 Discovering personas from dialogue data...")
    
    try:
        # Run persona discovery
        subprocess.run([sys.executable, "backend/persona_discovery.py"], check=True)
        print("✅ Persona discovery completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Persona discovery failed: {e}")
        return False

def check_environment():
    """Check if environment variables are set."""
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return False
    
    print("✅ Environment variables are configured")
    return True

def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print(f"❌ Some tests failed:\n{result.stdout}\n{result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def start_server():
    """Start the FastAPI server."""
    print("🚀 Starting FastAPI server...")
    print("📱 Frontend will be available at: http://localhost:8000")
    print("🔌 API documentation at: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "backend/api.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")

def main():
    """Main function to orchestrate the startup process."""
    print("🤖 Multi-Agent Conversational AI System")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check environment
    if not check_environment():
        return
    
    # Check if data files exist, if not process them
    if not check_data_files():
        print("📊 Data files not found. Processing data...")
        if not process_data():
            return
        if not discover_personas():
            return
    
    # Run tests
    print("\n🧪 Running tests...")
    run_tests()
    
    # Start server
    print("\n🚀 Starting the system...")
    start_server()

if __name__ == "__main__":
    main() 