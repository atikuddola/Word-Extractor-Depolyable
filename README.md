# PDF Word Extractor Web App

A Flask web application that extracts unique words from PDF files and allows users to download the results as a formatted PDF.

## Features

- Upload PDF files through a simple web interface
- Extract all unique words from PDF documents
- View extracted words in the browser
- Download extracted words as a formatted PDF file
- Responsive design for desktop and mobile devices

## Local Development

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

**Dependencies**:
- Flask (Web framework)
- PyPDF2 (PDF text extraction)
- reportlab (PDF generation)
- Werkzeug (File handling)
- gunicorn (WSGI server for deployment)

### Running Locally

```bash
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`

## Deployment to Vercel

### Prerequisites

- Vercel account
- Vercel CLI (optional)

### Deploy using Vercel CLI

1. Install Vercel CLI

```bash
npm install -g vercel
```

2. Login to Vercel

```bash
vercel login
```

3. Deploy the application

```bash
vercel
```

### Deploy using Vercel Dashboard

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Log in to your Vercel account
3. Click on 'New Project'
4. Import your repository
5. Configure the project settings:
   - Framework Preset: Other
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`
6. Click 'Deploy'

## Project Structure

- `app.py`: Main Flask application
- `extractor.py`: Core functionality for extracting words from PDFs
- `templates/`: HTML templates for the web interface
  - `layout.html`: Base template with styling
  - `index.html`: Upload page
  - `result.html`: Results page showing extracted words
- `vercel.json`: Configuration for Vercel deployment
- `requirements.txt`: Python dependencies

## Original CLI Usage

The original command-line functionality is still available:

```bash
python extractor.py input.pdf output.pdf
```

## Output Includes
- Numbered word list
- Total word count
- Clean formatting for printing/study
