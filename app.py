import os
import datetime
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
import tempfile
from extractor import extract_words_from_pdf

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-flask')
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract words from the PDF
            words = extract_words_from_pdf(filepath)
            # Remove duplicates and sort
            unique_words = sorted(set(words))
            
            # Clean up the uploaded file
            try:
                os.remove(filepath)
            except:
                pass  # Ignore errors in cleanup
            
            return render_template('result.html', 
                                   words=unique_words, 
                                   word_count=len(unique_words),
                                   total_words=len(words))
    
    return render_template('index.html')

# Add an API endpoint to get words as JSON (useful for potential future enhancements)
@app.route('/api/words', methods=['POST'])
def api_words():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract words from the PDF
        words = extract_words_from_pdf(filepath)
        # Remove duplicates and sort
        unique_words = sorted(set(words))
        
        # Clean up the uploaded file
        try:
            os.remove(filepath)
        except:
            pass  # Ignore errors in cleanup
            
        return jsonify({
            'words': unique_words,
            'word_count': len(unique_words),
            'total_words': len(words)
        })

# Handler for Vercel serverless function
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

# For local development
if __name__ == '__main__':
    app.run(debug=True)
