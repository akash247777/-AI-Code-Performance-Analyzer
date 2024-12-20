# AI-Code-Performance-Analyzer

# Overview

A Streamlit-based tool for analyzing Python code performance, identifying potential bottlenecks, and providing optimization suggestions.

# Features

Upload Python files or paste code directly
Detect nested loop complexities
Identify inefficient string operations
Analyze memory usage
Profile execution time
Provide optimization suggestions

# Setup & Installation

# Prerequisites

* Python 3.8+
* pip

# Installation Steps

1. Clone the repository
   
       git clone https://github.com/yourusername/performance-analyzer.git
   
       cd performance-analyzer
    

2. Create a virtual environment

           python -m venv venv
   
           source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install dependencies

            pip install -r requirements.txt
4. Run the Streamlit app

        streamlit run performance_analyzer.py
# Usage

   1. Choose between pasting code or uploading a Python file
   2. Click "Analyze Performance"
   3. Review bottlenecks, memory usage, and execution profile

# Limitations

 * Experimental performance detection
 * Primarily static code analysis
 * May not catch all performance issues

# Contributing 

Contributions are welcome! Please open an issue or submit a pull request.
