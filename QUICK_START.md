# Quick Start Guide

Get the Omani Legal AI Assistant up and running in just a few minutes.

## 1. Set Up Environment

### In Replit

1. Fork this Replit project
2. Go to "Secrets" in the sidebar and add:
   - `OPENAI_API_KEY` with your OpenAI API key value
   - (Optional) `ANTHROPIC_API_KEY` with your Anthropic API key value
3. Click "Run" at the top of the page

### Local Setup

```bash
# Clone repository
git clone https://github.com/alanqoudif/Omani-Legal-AI-Assistant.git
cd omani-legal-ai-assistant

# Install dependencies 
pip install -r requirements.txt

# Set API key
# On Linux/Mac:
export OPENAI_API_KEY="your-api-key-here"
# On Windows:
set OPENAI_API_KEY=your-api-key-here

# Run the application
streamlit run app.py --server.port 5000
```

## 2. Upload Documents

1. Open the application in your browser
2. Select "Process Legal Documents" from the sidebar
3. Upload PDF files containing legal documents (e.g., Omani laws, regulations)
4. Wait for processing to complete

## 3. Start Using Features

### Document Q&A
- Type a question or upload an audio file
- Click "Ask Question" to get an answer

### Article Summarizer
- Select a law
- Enter an article number
- Click "Summarize" to get a concise summary

### Law Comparison
- Select two different laws
- Click "Compare" to see a detailed comparison

### Case Analyzer
- Describe a legal case
- Click "Analyze" to get relevant legal analysis
- Download the PDF report for your records

### Document Creator
- Select a document type
- Enter specifications
- Click "Generate" to create a custom legal document

## 4. Language Options

- Toggle between English and Arabic using the language selector in the sidebar
- All features support both languages

## 5. Voice Input

- Upload audio files (WAV, MP3, OGG) using the voice input feature
- The system will transcribe your voice to text automatically

## Need More Help?

- See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions
- Check the [README.md](README.md) for complete documentation
- Visit the project repository for the latest updates