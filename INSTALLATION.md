# Detailed Installation Guide

This document provides comprehensive installation instructions for setting up the Omani Legal AI Assistant on different platforms.

## Required Python Packages

```
# Core dependencies
streamlit>=1.26.0
openai>=1.0.0
anthropic>=0.5.0
langchain>=0.0.292
langchain-community>=0.0.10
numpy>=1.24.0
faiss-cpu>=1.7.4
google-generativeai>=0.3.0

# Document processing
pymupdf>=1.22.0
reportlab>=4.0.0
pydub>=0.25.1
trafilatura>=1.6.0

# Arabic text support
arabic-reshaper>=3.0.0
python-bidi>=0.4.2

# Audio processing
whisper>=1.1.10
tensorflow>=2.13.0
tensorflow-hub>=0.14.0

# For vector embeddings
sentence-transformers>=2.2.2
```

## Installation Steps

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment tool (recommended)
- OpenAI API key
- (Optional) Anthropic API key

### On Windows

1. **Install Python**:
   - Download and install Python from [python.org](https://www.python.org/downloads/windows/)
   - Make sure to check "Add Python to PATH" during installation

2. **Create a virtual environment** (recommended):
   ```
   mkdir omani-legal-ai
   cd omani-legal-ai
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Clone or download the project**:
   ```
   git clone <repository-url> .
   # OR download and extract the ZIP file
   ```

4. **Install dependencies**:
   ```
   pip install streamlit openai langchain langchain-community numpy faiss-cpu pymupdf reportlab
   pip install pydub trafilatura arabic-reshaper python-bidi tensorflow tensorflow-hub
   pip install sentence-transformers google-generativeai anthropic
   ```

5. **Set environment variables**:
   ```
   set OPENAI_API_KEY=your-openai-api-key
   set ANTHROPIC_API_KEY=your-anthropic-api-key (optional)
   ```

6. **Run the application**:
   ```
   streamlit run app.py --server.port 5000
   ```

### On macOS/Linux

1. **Install Python**:
   ```
   # On macOS with Homebrew
   brew install python

   # On Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Create a virtual environment** (recommended):
   ```
   mkdir omani-legal-ai
   cd omani-legal-ai
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Clone or download the project**:
   ```
   git clone <repository-url> .
   # OR download and extract the ZIP file
   ```

4. **Install dependencies**:
   ```
   pip install streamlit openai langchain langchain-community numpy faiss-cpu pymupdf reportlab
   pip install pydub trafilatura arabic-reshaper python-bidi tensorflow tensorflow-hub
   pip install sentence-transformers google-generativeai anthropic
   ```

5. **Set environment variables**:
   ```
   export OPENAI_API_KEY="your-openai-api-key"
   export ANTHROPIC_API_KEY="your-anthropic-api-key" # optional
   ```

6. **Run the application**:
   ```
   streamlit run app.py --server.port 5000
   ```

### Using Docker (Advanced)

1. **Create a Dockerfile**:
   ```
   FROM python:3.9-slim

   WORKDIR /app

   COPY . .

   RUN pip install --no-cache-dir streamlit openai langchain langchain-community numpy faiss-cpu pymupdf reportlab pydub trafilatura arabic-reshaper python-bidi tensorflow tensorflow-hub sentence-transformers google-generativeai anthropic

   EXPOSE 5000

   CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
   ```

2. **Build and run the Docker container**:
   ```
   docker build -t omani-legal-ai .
   docker run -p 5000:5000 -e OPENAI_API_KEY="your-openai-api-key" omani-legal-ai
   ```

## Troubleshooting

### Common Issues

1. **Missing dependencies**:
   - If you encounter errors about missing modules, install them individually:
   ```
   pip install <module-name>
   ```

2. **API Key errors**:
   - Ensure your API keys are correctly set in environment variables
   - Check that the API keys are valid and have sufficient credits

3. **PDF processing issues**:
   - Make sure you have the correct version of pymupdf:
   ```
   pip install --upgrade pymupdf
   ```

4. **Arabic text rendering problems**:
   - Verify arabic-reshaper and python-bidi are installed:
   ```
   pip install arabic-reshaper python-bidi
   ```

5. **Audio processing errors**:
   - For issues with audio processing, ensure whisper and pydub are installed:
   ```
   pip install whisper pydub
   ```
   - You might need to install ffmpeg:
     - On Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
     - On macOS: `brew install ffmpeg`
     - On Ubuntu/Debian: `sudo apt install ffmpeg`

6. **Port in use**:
   - If port 5000 is already in use, change to a different port:
   ```
   streamlit run app.py --server.port 8501
   ```

## Updating

To update to the latest version:

1. **Pull the latest changes** (if using git):
   ```
   git pull origin main
   ```

2. **Update dependencies**:
   ```
   pip install --upgrade streamlit openai langchain langchain-community
   ```

## Alternative Installation Methods

### Using pip requirements file (create manually)

1. Create a file named `requirements.txt` with the package list from the top of this document
2. Install all packages at once:
   ```
   pip install -r requirements.txt
   ```

### Using Conda

1. **Create a conda environment**:
   ```
   conda create -n legal-ai python=3.9
   conda activate legal-ai
   ```

2. **Install dependencies**:
   ```
   conda install -c conda-forge streamlit numpy
   pip install openai langchain langchain-community faiss-cpu pymupdf reportlab pydub trafilatura arabic-reshaper python-bidi tensorflow tensorflow-hub sentence-transformers google-generativeai anthropic
   ```

## For Development

If you're planning to contribute to the project:

1. **Install development tools**:
   ```
   pip install black flake8 pytest
   ```

2. **Set up pre-commit** (optional):
   ```
   pip install pre-commit
   pre-commit install
   ```