from flask import Flask, request, jsonify
import spacy
import pdfplumber

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    file = request.files["resume"]
    text = extract_text_from_pdf(file)
    doc = nlp(text)

    skills = [token.text for token in doc if token.pos_ == "NOUN"]
    return jsonify({"skills": list(set(skills))})

if __name__ == "__main__":
    app.run(debug=True)
