
```markdown
# RAG Demo - TechCorp Company Knowledge Base

A Flask web application that demonstrates Retrieval-Augmented Generation (RAG) using Google's Gemini AI to provide accurate company-specific information.

## Features

- **RAG Implementation**: Shows how RAG enhances AI responses with company-specific knowledge
- **Company Knowledge Base**: Comprehensive information about TechCorp including policies, products, and procedures
- **Dual Response Comparison**: Compare RAG-enhanced responses vs direct AI responses
- **Environment Variable Configuration**: Secure API key management
- **Responsive Design**: Works on desktop and mobile devices

## Setup Instructions

### 1. Clone or Download the Project

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**To get your Gemini API key:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

### 4. Run the Application

```bash
python app.py
```

### 5. Open Your Browser

Navigate to `http://localhost:5000`

## Project Structure

```
rag-demo/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md             # This file
├── templates/
│   ├── index.html        # Homepage template
│   └── result.html       # Results page template
└── static/
    └── style.css         # CSS styles
```

## How RAG Works in This Demo

1. **Retrieval**: When you ask a question, the system searches through the company knowledge base for relevant information
2. **Augmentation**: The retrieved information is combined with your original question
3. **Generation**: Gemini AI generates a response using both your question and the retrieved context

## Example Questions to Try

- **Company Info**: "Who are the founders?" "What does TechCorp do?"
- **HR Policies**: "What's the vacation policy?" "How does remote work work?"
- **Products**: "How much does the Pro plan cost?" "What new features are coming?"
- **Procedures**: "How do expense reimbursements work?" "When are performance reviews?"

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini API
- **Frontend**: HTML, CSS, JavaScript
- **Configuration**: python-dotenv

## API Models Used

The application automatically uses the best available Gemini model:
- Primary: `gemini-2.0-flash-exp` (latest)
- Fallback: `gemini-1.5-flash` (widely available)

## Troubleshooting

### Common Issues:

1. **API Key Error**: Make sure your `.env` file exists and contains a valid Gemini API key
2. **Module Not Found**: Run `pip install -r requirements.txt` to install all dependencies
3. **Port Already in Use**: Change the port in `app.py` or stop other applications using port 5000

### Getting Help:

If you encounter issues:
1. Check that your API key is valid and has sufficient quotas
2. Verify all dependencies are installed correctly
3. Check the console for error messages when starting the application

## License

This project is for demonstration purposes.
```

## 5. Updated Project Structure:

```
rag-demo/
├── app.py
├── requirements.txt
├── .env                    # Create this file
├── README.md
├── templates/
│   ├── index.html
│   └── result.html
└── static/
    └── style.css
```

## 6. Setup Commands:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Key Changes Made:

1. **Environment Variables**: Used `python-dotenv` to load API key from `.env` file
2. **Model Selection**: Added automatic model detection with fallbacks
3. **Better Error Handling**: Improved error messages and fallback responses
4. **Documentation**: Comprehensive README and requirements file
5. **Security**: API key is no longer hardcoded in the source code

The application will now:
- Load your API key securely from the `.env` file
- Automatically use the best available Gemini model
- Provide clear error messages if something goes wrong
- Work with fallback responses even if the API is unavailable

Just create the `.env` file with your API key and run `python app.py` to start the demo!