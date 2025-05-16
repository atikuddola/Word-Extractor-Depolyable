import os
import datetime
from flask import Flask, request, render_template, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
import tempfile
from extractor import extract_words_from_pdf, save_words_to_pdf

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
            
            # Create a temporary file for the output PDF
            output_fd, output_path = tempfile.mkstemp(suffix='.pdf')
            os.close(output_fd)
            
            # Save words to PDF
            save_words_to_pdf(unique_words, output_path)
            
            # Store the output path in a temporary dictionary
            session_id = os.path.basename(output_path)
            # Use a global dictionary to store paths (for Vercel compatibility)
            if not hasattr(app, 'temp_files'):
                app.temp_files = {}
            app.temp_files[session_id] = output_path
            
            return render_template('result.html', 
                                   words=unique_words, 
                                   word_count=len(unique_words),
                                   total_words=len(words),
                                   session_id=session_id)
    
    return render_template('index.html')

@app.route('/download/<session_id>')
def download(session_id):
    if not hasattr(app, 'temp_files'):
        app.temp_files = {}
    output_path = app.temp_files.get(session_id)
    if not output_path or not os.path.exists(output_path):
        flash('File not found or expired')
        return redirect(url_for('index'))
    
    return send_file(output_path, as_attachment=True, download_name='extracted_words.pdf')

# Add cleanup for temporary files
@app.teardown_appcontext
def cleanup(exception):
    # Remove temporary files older than 1 hour
    pass  # Implement if needed

# Handler for Vercel serverless function
def handler(environ, start_response):
    return app.wsgi_app(environ, start_response)

# For local development
if __name__ == '__main__':
    app.run(debug=True)
