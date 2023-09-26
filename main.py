from flask import Flask,render_template,url_for, request, jsonify,redirect
import json
from google.oauth2 import service_account
import gspread
import pandas as pd
from notmain import notmainBlueprint
# from transformers import pipeline
from docx import Document
from werkzeug.utils import secure_filename


app = Flask("__name__")
app.register_blueprint(notmainBlueprint,url_prefix = "/faq")
credentials = service_account.Credentials.from_service_account_file(
    "static/data/indian-legal-information-d6444bb36676.json",
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

spreadsheet_id = '1KHrJxFzRNfCFM3POGqdXvTjXmoZG9Cx79vNeznaFPQI'

client = gspread.authorize(credentials)
sheet = client.open_by_key(spreadsheet_id).sheet1



@app.route("/")
def home():
    return render_template("home.html")

@app.route("/readdressal")
def readdressal():
    return render_template("readdressal.html")

@app.route("/law-and-regulations")
def Lawandregulations():
    return render_template("Lawandregulations.html")

@app.route("/legal-aid")
def legalaid():
    return render_template("legalaid.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route('/documents')
def documents():
    return render_template('Documents.html', summary=None)


# @app.route('/summarize', methods=['POST'])
# def summarize():
#     document = request.files['document']
#     if document:
#         if document.filename.endswith('.txt'):
#             doc_text = document.read().decode('utf-8')
#         else:
#             doc = Document(document)
#             formatted_text = ""
#             for paragraph in doc.paragraphs:
#                 if paragraph.text.strip(): 
#                     formatted_text += paragraph.text + "\n"      
#             f = open('static/data/text.txt', 'r', errors='ignore', encoding='utf-8')
#             text = f.read()
#             summarizer = pipeline("summarization")
#             summary = summarizer(formatted_text, text)  
#             return render_template('Documents.html', summary=summary[0]['summary_text'])       
#         f = open('static/data/text.txt', 'r', errors='ignore', encoding='utf-8')
#         text = f.read()
#         summarizer = pipeline("summarization")
#         summary = summarizer(doc_text, text)
#         print(summary)
#         if summary:
#             return render_template('Documents.html', summary=summary[0]['summary_text'])
#         else:
#             return render_template('Documents.html', summary="No summary available")  
#     return redirect(url_for('documents'))

def convert_sheet_to_json(df):
    json_data = []
    current_rights = None
    current_articles = []
    current_desc = []

    for index,row in df.iterrows():
        if not pd.isnull(row['RIGHTS']):
            if current_rights is not None:
                json_data.append({'RIGHTS': current_rights, 'LIST_OF_ARTICLES': current_articles, 'DESCRIPTION': current_desc})
            current_rights = row['RIGHTS']
            current_articles = []
            current_desc = []
        if not pd.isnull(row['LIST_OF_ARTICLES']):
            current_articles.append(row['LIST_OF_ARTICLES'])
        if not pd.isnull(row['DESCRIPTION']):
            current_desc.append(row['DESCRIPTION'])

    if current_rights is not None:
        json_data.append({'RIGHTS': current_rights, 'LIST_OF_ARTICLES': current_articles, 'DESCRIPTION': current_desc})

    json_string = json.dumps(json_data, indent=4)

    return json_string

df = pd.DataFrame(sheet.get_all_records())
data_json = convert_sheet_to_json(df)

data = json.loads(data_json)

def group_data_by_right(data):
    right_data = {}
    for entry in data:
        right = entry["RIGHTS"]
        if right not in right_data:
            right_data[right] = {"LIST_OF_ARTICLES": [], "DESCRIPTION": []}
        right_data[right]["LIST_OF_ARTICLES"].extend(entry["LIST_OF_ARTICLES"])
        right_data[right]["DESCRIPTION"].extend(entry["DESCRIPTION"])
    return right_data

grouped_data = group_data_by_right(data)

@app.route('/legal-rights', methods=['GET'])
def legalrights():
    return render_template('legalrights.html', grouped_data=grouped_data)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    results = []

    if not query:
        return jsonify(data)

    for entry in data:
        if entry["RIGHTS"] == query:
            results.append(entry)

    return jsonify(results)



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)