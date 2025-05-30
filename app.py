from flask import Flask, jsonify, request
from app.services.db_service import save_candidate, get_candidates, get_candidate_by_id
from app.services.email_service import fetch_resume_emails
from app.services.resume_parser import extract_text_from_pdf, extract_text_from_docx, parse_resume_text
import os

app = Flask(__name__)

@app.route('/api/harvest', methods=['POST'])
def harvest_resumes():
    files = fetch_resume_emails()
    candidates = []
    for file in files:
        if file.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif file.endswith('.docx'):
            text = extract_text_from_docx(file)
        else:
            continue
        candidate = parse_resume_text(text)
        candidate['filename'] = os.path.basename(file)
        save_candidate(candidate)
        candidates.append(candidate)
    return jsonify({'harvested': len(candidates), 'candidates': candidates})

@app.route('/api/candidates', methods=['GET'])
def list_candidates():
    result = get_candidates()
    for candidate in result:
        candidate['_id'] = str(candidate['_id'])
    return jsonify(result)

@app.route('/api/candidates/<candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    candidate = get_candidate_by_id(candidate_id)
    if candidate:
        candidate['_id'] = str(candidate['_id'])
        return jsonify(candidate)
    return jsonify({'error': 'Not found'}), 404

@app.route('/')
def home():
    return "Flask is running!"

if __name__ == '__main__':
    app.run(debug=True)
