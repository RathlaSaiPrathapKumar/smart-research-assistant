# Smart Assistant for Research Summarization

## 📋 Project Overview

A comprehensive AI-powered tool that helps users interact with research documents, legal files, technical manuals, and other structured reports. The assistant provides intelligent document analysis, automatic summarization, question-answering capabilities, and interactive learning challenges.

## 🎯 Key Features

### 📄 Document Processing
- **Multi-format Support**: Upload PDF and TXT documents
- **Text Extraction**: Automatic extraction and processing of document content
- **Document Preview**: View first 500 characters of uploaded documents

### 🤖 Auto Summary Generation
- **AI-Powered Summarization**: Uses Facebook BART-large-CNN model
- **Concise Output**: Generates summaries ≤ 150 words
- **Smart Chunking**: Handles long documents by processing in chunks
- **Performance Optimized**: Limits processing to first 3 chunks for efficiency

### ❓ Ask Anything Mode
- **Contextual Q&A**: Ask any question about the uploaded document
- **AI-Powered Answers**: Uses DistilBERT model for question answering
- **Document-Grounded Responses**: All answers are based on document content
- **Justification System**: Provides references from the document for each answer
- **No Hallucination**: Ensures answers are directly supported by the source material

### 🎯 Challenge Me Mode
- **Dynamic Question Generation**: Creates 3 logic-based questions per session
- **Fresh Questions**: Generates new questions every time (no repetition)
- **Interactive Learning**: Answer questions and receive immediate feedback
- **Smart Evaluation**: Analyzes answer quality using word overlap analysis
- **Reference System**: Shows relevant document sections for each question
- **Multiple Question Types**: 
  - Content-specific questions based on document sentences
  - Generic comprehension questions
  - Methodology and argument analysis

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **NLP Models**: Hugging Face Transformers
  - Summarization: `facebook/bart-large-cnn`
  - Question Answering: `distilbert-base-uncased-distilled-squad`
- **Text Processing**: 
  - PDF Extraction: `pdfminer.six`
  - Natural Language Processing: `nltk`
- **Document Handling**: Built-in Python libraries (`io`, `stringio`)

### Core Components

#### 1. Document Upload & Processing
```python
# PDF Processing
text = extract_text(uploaded_file)

# TXT Processing  
stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
text = stringio.read()
```

#### 2. Summarization Engine
```python
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# Chunks text for processing, limits to 150 words
```

#### 3. Question Answering System
```python
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
# Uses document context to answer user questions
```

#### 4. Challenge Question Generator
```python
# Extracts key concepts from document sentences
# Generates contextual questions with document references
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or later
- Windows/macOS/Linux

### Step 1: Clone or Download Project
```bash
# Navigate to your project directory
cd path/to/your/project
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv assistant_env

# Activate virtual environment
# Windows:
assistant_env\Scripts\activate
# macOS/Linux:
source assistant_env/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Download NLTK Data
```bash
# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### Step 5: Run the Application
```bash
# Start the Streamlit app
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage Guide

### Getting Started
1. **Upload Document**: Click "Browse files" to upload a PDF or TXT document
2. **View Summary**: The app automatically generates a concise summary
3. **Choose Mode**: Use either "Ask Anything" or "Challenge Me" mode

### Ask Anything Mode
1. **Enter Question**: Type any question about the document
2. **Get Answer**: Receive AI-generated answer with justification
3. **Review Reference**: See the specific document section supporting the answer

### Challenge Me Mode
1. **Generate Questions**: Click "Generate Challenge Questions"
2. **Answer Questions**: Fill in the text areas for each question
3. **Submit for Evaluation**: Click "Submit Answers for Evaluation"
4. **Review Feedback**: See evaluation results with document references
5. **Generate New Questions**: Click "Generate New Questions" for fresh challenges

## 🔧 Technical Details

### Dependencies
```
streamlit==1.46.1
transformers==4.53.0
torch==2.7.1
pdfminer.six==20250506
nltk==3.9.1
pandas==2.3.0
```

### Model Specifications
- **Summarization Model**: BART-large-CNN (1.6GB)
- **QA Model**: DistilBERT-base-uncased (268MB)
- **Processing Limit**: 2000 characters for QA context
- **Summary Length**: ≤ 150 words

### Performance Optimizations
- **Text Chunking**: Processes documents in 1000-character chunks
- **Context Limiting**: Uses first 2000 characters for QA
- **Session State**: Manages question generation efficiently
- **Error Handling**: Graceful fallbacks for missing NLTK data

## 🎨 User Interface Features

### Responsive Design
- **Wide Layout**: Optimized for desktop viewing
- **Clear Sections**: Well-organized interface with distinct modes
- **Progress Indicators**: Loading spinners for long operations
- **Success/Error Messages**: Clear feedback for all operations

### Interactive Elements
- **File Upload**: Drag-and-drop or browse functionality
- **Text Input**: Real-time question input
- **Text Areas**: Multi-line answer input for challenges
- **Buttons**: Clear action buttons with loading states

## 🔍 Evaluation System

### Answer Quality Assessment
- **Word Overlap Analysis**: Compares user answers with document content
- **Three-Tier Evaluation**:
  - ✅ **Good Answer**: Significant word overlap (>2 words)
  - ⚠️ **Partial Answer**: Some overlap, needs improvement
  - ❌ **No Answer**: Empty or insufficient response

### Reference System
- **Document Citations**: Shows exact sentences from source material
- **Context Preservation**: Maintains document context for answers
- **Justification Display**: Clear explanation of evaluation criteria

## 🚀 Future Enhancements

### Potential Improvements
- **Advanced Question Generation**: Use dedicated question generation models
- **Multi-language Support**: Extend to other languages
- **Document Comparison**: Compare multiple documents
- **Export Features**: Save summaries and Q&A sessions
- **User Authentication**: Multi-user support with session management
- **API Integration**: RESTful API for external applications

### Model Upgrades
- **Larger Context Windows**: Handle longer documents more effectively
- **Specialized Models**: Domain-specific models for different document types
- **Real-time Processing**: Stream processing for large documents

## 🐛 Troubleshooting

### Common Issues

#### NLTK Data Missing
```bash
# Solution: Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

#### Streamlit Not Found
```bash
# Solution: Install streamlit in activated environment
pip install streamlit
```

#### Model Download Issues
- **Slow Download**: Models are large (1-2GB), ensure stable internet
- **Memory Issues**: Close other applications to free up RAM
- **Disk Space**: Ensure sufficient disk space for model downloads

### Performance Tips
- **Document Size**: Optimal for documents under 50 pages
- **Question Complexity**: Simple, direct questions work best
- **Browser**: Use modern browsers (Chrome, Firefox, Safari)

## 📄 License

This project is developed for educational and research purposes. Please ensure compliance with the licenses of the underlying models and libraries used.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📞 Support

For technical support or questions about the project, please open an issue in the project repository.

---

**Built with ❤️ using Streamlit, Hugging Face Transformers, and Python** 