# Omani Legal AI Assistant

A bilingual Legal AI Assistant specialized in Omani legal documentation, offering advanced document processing capabilities across Arabic and English languages.

## Features

- **Document Q&A**: Ask questions about legal documents in English or Arabic
- **Article Summarization**: Get concise summaries of specific legal articles
- **Law Comparison**: Compare different laws to understand similarities and differences
- **Case Analysis**: Submit a case description and get legal analysis based on relevant laws
- **Document Creation**: Generate legal documents based on user specifications
- **Voice Input**: Upload voice recordings for hands-free interaction
- **AI-Powered Text Improvement**: Enhanced readability for legal citations
- **PDF Generation**: Export results as professional PDF documents
- **Bilingual Support**: Full support for both English and Arabic

## Prerequisites

- Python 3.9 or higher
- OpenAI API key
- (Optional) Anthropic API key for alternative model support

## Installation

### Option 1: Using Replit

1. Fork this Replit project
2. Set up your environment secrets:
   - Go to the "Secrets" tab in your Replit project
   - Add your `OPENAI_API_KEY` as a new secret
   - (Optional) Add `ANTHROPIC_API_KEY` if you want to use Claude models

3. Run the application:
   - Click the "Run" button at the top
   - The application will start at the URL shown in the console

### Option 2: Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/alanqoudif/Omani-Legal-AI-Assistant.git
   cd omani-legal-ai-assistant
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

   Required packages include:
   - streamlit
   - openai
   - anthropic (optional)
   - langchain
   - langchain-community
   - numpy
   - faiss-cpu
   - google-generativeai
   - pymupdf
   - reportlab
   - pydub
   - trafilatura
   - arabic-reshaper
   - python-bidi
   - whisper
   - tensorflow
   - tensorflow-hub
   - sentence-transformers

3. Set up environment variables:
   ```
   # On Linux/Mac
   export OPENAI_API_KEY="your-openai-api-key"
   
   # On Windows
   set OPENAI_API_KEY=your-openai-api-key
   ```

4. Run the application:
   ```
   streamlit run app.py --server.port 5000
   ```

## Using the Application

1. **Process Legal Documents**:
   - Click on "Process Legal Documents" to upload PDF files of legal documents
   - The system will process and index the documents for searching

2. **Document Q&A**:
   - Ask questions about the legal documents
   - Use voice input by clicking the microphone button or uploading an audio file
   - View responses with improved text formatting

3. **Article Summarizer**:
   - Select a law and article number
   - Get a concise summary of the article

4. **Law Comparison**:
   - Select two different laws
   - View a detailed comparison highlighting similarities and differences

5. **Case Analyzer**:
   - Describe a legal case
   - Receive analysis based on relevant laws
   - Download a PDF report

6. **Document Creator**:
   - Specify details for a legal document
   - Get a professionally formatted document

## Language Support

- Toggle between English and Arabic using the language selector
- All components support both languages
- Arabic text is properly handled with bidirectional support

## API Keys

This application uses OpenAI's GPT models for text processing. You'll need to provide your own API key:

1. Get an API key from [OpenAI](https://platform.openai.com/account/api-keys)
2. Add it to your environment variables as `OPENAI_API_KEY`

For Claude model support:
1. Get an API key from [Anthropic](https://console.anthropic.com/account/keys)
2. Add it to your environment variables as `ANTHROPIC_API_KEY`

## Troubleshooting

- **Application not starting**: Ensure all dependencies are installed and API keys are set up
- **PDF processing errors**: Make sure PDFs are not encrypted and are in a readable format
- **Arabic text display issues**: Verify that arabic-reshaper and python-bidi are installed correctly
- **Voice input not working**: Check that audio files are in supported formats (WAV, MP3, OGG)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project uses various AI models and libraries for natural language processing
- Special thanks to the Streamlit, Langchain, and OpenAI communities for their tools and documentation