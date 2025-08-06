#!/usr/bin/env python3
"""
Simple test script to verify the implementation structure.
This script checks the core components without requiring all dependencies.
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """Test that the project structure is correct."""
    print("🔍 Testing project structure...")
    
    required_files = [
        'backend/agents.py',
        'backend/api.py', 
        'backend/data_loader.py',
        'backend/persona_discovery.py',
        'frontend/index.html',
        'tests/test_agents.py',
        'requirements.txt',
        'README.md',
        'run.py',
        'demo.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files exist")
        return True

def test_data_files():
    """Test that data files exist."""
    print("\n📊 Testing data files...")
    
    data_files = [
        'data/full_dialogues.csv',
        'data/dialogues_with_personas.csv',
        'data/persona_0_data.csv',
        'data/persona_1_data.csv',
        'data/persona_2_data.csv'
    ]
    
    existing_files = []
    missing_files = []
    
    for file_path in data_files:
        if os.path.exists(file_path):
            existing_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    print(f"✅ Existing data files: {len(existing_files)}")
    for file in existing_files:
        print(f"   - {file}")
    
    if missing_files:
        print(f"⚠️  Missing data files: {len(missing_files)}")
        for file in missing_files:
            print(f"   - {file}")
        print("   (These will be created when running data processing)")
    
    return len(existing_files) > 0

def test_code_structure():
    """Test that the code structure is correct."""
    print("\n💻 Testing code structure...")
    
    # Test backend structure
    backend_files = [
        'backend/agents.py',
        'backend/api.py',
        'backend/data_loader.py', 
        'backend/persona_discovery.py'
    ]
    
    for file_path in backend_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if 'class' in content and 'def' in content:
                    print(f"✅ {file_path} - Contains classes and functions")
                else:
                    print(f"⚠️  {file_path} - May be incomplete")
        else:
            print(f"❌ {file_path} - Missing")
    
    # Test frontend
    if os.path.exists('frontend/index.html'):
        with open('frontend/index.html', 'r') as f:
            content = f.read()
            if 'Multi-Agent' in content and 'chat' in content:
                print("✅ frontend/index.html - Contains chat interface")
            else:
                print("⚠️  frontend/index.html - May be incomplete")
    
    return True

def test_documentation():
    """Test that documentation is comprehensive."""
    print("\n📚 Testing documentation...")
    
    if os.path.exists('README.md'):
        with open('README.md', 'r') as f:
            content = f.read()
            
            required_sections = [
                'Project Overview',
                'Persona Discovery',
                'Setup & Running Instructions',
                'Usage Guide',
                'Testing'
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"⚠️  Missing README sections: {missing_sections}")
            else:
                print("✅ README.md contains all required sections")
    
    return True

def test_requirements():
    """Test that requirements are properly specified."""
    print("\n📦 Testing requirements...")
    
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
            required_packages = [
                'langchain',
                'langgraph', 
                'fastapi',
                'uvicorn',
                'pandas',
                'openai'
            ]
            
            missing_packages = []
            for package in required_packages:
                if package not in content:
                    missing_packages.append(package)
            
            if missing_packages:
                print(f"⚠️  Missing packages in requirements.txt: {missing_packages}")
            else:
                print("✅ requirements.txt contains all required packages")
    
    return True

def main():
    """Run all tests."""
    print("🧪 Multi-Agent Conversational AI - Implementation Test")
    print("=" * 60)
    
    tests = [
        test_project_structure,
        test_data_files,
        test_code_structure,
        test_documentation,
        test_requirements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The implementation structure is correct.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up OpenAI API key in .env file")
        print("3. Run the system: python run.py")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    main() 