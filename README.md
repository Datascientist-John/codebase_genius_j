GitHub Documentation Generator
An AI-powered web application that automatically generates comprehensive documentation for GitHub repositories using Google's Gemini 2.0 Flash model.

 Features
AI-Powered Analysis: Leverages Gemini 2.0 Flash for intelligent code analysis
Simple GitHub Integration: Just paste a repository URL
Comprehensive Documentation: Generates detailed documentation in JSON format
Generation History: Track all your previous documentation generations
Easy Export: Download generated documentation as JSON files
Modern UI: Clean, intuitive interface built with Streamlit
Health Monitoring: Built-in server health check functionality

Getting Started
Prerequisites
Python
Jac backend server
Internet connection

Installation

Clone the repository

Install dependencies

bash   pip install streamlit requests

Start the Jac backend server

bash   jac serve main.jac
The server should be running on http://localhost:8000

Launch the Streamlit app

bash streamlit run  streamlit_app.py

Open your browser
The app will automatically open at http://localhost:8501

Check Server Status: Click the "Check Health" button in the sidebar to ensure the backend is running
Enter Repository URL: Paste a valid GitHub repository URL in the format:

   https://github.com/username/repository

Generate Documentation: Click the "Generate" button and wait for the AI to analyze the repository
Review Results: The generated documentation will appear in JSON format
Download: Use the download button to save the documentation locally
View History: Access previous generations from the history section

 Architecture
┌─────────────────┐         ┌─────────────────┐
│                 │  HTTP   │                 │
│   Streamlit     ├────────►│      Jac        │
│   Frontend      │         │   (Backend)     │
│                 │◄────────┤                 │
└─────────────────┘  JSON   └─────────────────┘
                                     │
                                     │ API Call
                                     ▼
                             ┌──────────────┐
                             │   Gemini     │
                             │  2.0 Flash   │
                             └──────────────┘
Configuration
The application uses the following default endpoints:

Base URL: http://localhost:8000
Generate Docs: /walker/generate_docs
Health Check: /walker/health_check



Check backend server logs
Verify the backend is returning proper JSON format

Contributions are welcome! Please feel free to submit a Pull Request.
