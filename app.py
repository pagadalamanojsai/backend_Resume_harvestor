from flask import Flask, jsonify, request
from app.services.db_service import save_candidate, get_candidates, get_candidate_by_id
from app.services.email_service import fetch_resume_emails
from app.services.resume_parser import extract_text_from_pdf, extract_text_from_docx, parse_resume_text
import os
import requests
import csv

print("CWD:", os.getcwd())
print("App started!")

SPREADSHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1z8kjLvFh9nK18Jhihg7frVux-6k3vdT28NQKuWbUdyM/export?format=csv"
ATTACHMENTS_DIR = "attachments"

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is running!"

@app.route('/hello')
def hello():
    print("Hello route was hit!")
    return "Hello!"

def harvest_from_google_sheet():
    # Download the latest CSV from Google Sheets
    response = requests.get(SPREADSHEET_CSV_URL)
    response.raise_for_status()
    csv_content = response.content.decode('utf-8')

    # Ensure attachments directory exists
    if not os.path.exists(ATTACHMENTS_DIR):
        os.makedirs(ATTACHMENTS_DIR)

    candidates = []
    reader = csv.DictReader(csv_content.splitlines())
    for row in reader:
        url = row.get('resume_link')  # Change if your column name is different
        if not url:
            continue
        filename = url.split('/')[-1].split('?')[0]
        local_path = os.path.join(ATTACHMENTS_DIR, filename)

        # Download resume
        try:
            r = requests.get(url)
            r.raise_for_status()
            with open(local_path, 'wb') as f:
                f.write(r.content)
        except Exception as e:
            print(f"Could not download {url}: {e}")
            continue

        # Parse the file
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(local_path)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(local_path)
        else:
            continue
        candidate = parse_resume_text(text)
        candidate['filename'] = filename
        save_candidate(candidate)
        candidates.append(candidate)
    return candidates

@app.route('/api/harvest', methods=['POST'])
def harvest_resumes():
    print("Harvest endpoint was hit!")
    candidates = harvest_from_google_sheet()
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)
