import json
from flask import Flask, render_template, request, jsonify,Blueprint
from google.oauth2 import service_account
import gspread
import pandas as pd

notmainBlueprint = Blueprint("notmain",__name__, template_folder="templates")


credentials = service_account.Credentials.from_service_account_file(
    "static/data/indian-legal-information-d6444bb36676.json",
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)


spreadsheet_id = '18Yq6ap93DjQjy0HCceGL15bejKmQjyvX7tE1QQSLeR8'

client = gspread.authorize(credentials)
sheet = client.open_by_key(spreadsheet_id).sheet1

def convert_sheet_to_json_faqs(df):
    json_data = []
    current_law = None
    current_questions = []
    current_answers = []

    for index,row in df.iterrows():
        if not pd.isnull(row['LAW']):
            if current_law is not None:
                json_data.append({'LAW': current_law, 'QUESTIONS': current_questions, 'ANSWERS': current_answers})
            current_law = row['LAW']
            current_questions = []
            current_answers = []
        if not pd.isnull(row['QUESTION']):
            current_questions.append(row['QUESTION'])
        if not pd.isnull(row['ANSWER']):
            current_answers.append(row['ANSWER'])

    if current_law is not None:
        json_data.append({'LAW': current_law, 'QUESTIONS': current_questions, 'ANSWERS': current_answers})

    json_string = json.dumps(json_data, indent=4)

    return json_string

df_faqs = pd.DataFrame(sheet.get_all_records())
data_json_faqs = convert_sheet_to_json_faqs(df_faqs)

data_faqs = json.loads(data_json_faqs)

def group_data_by_law_faqs(data_faqs):
    law_data = {}
    for entry in data_faqs:
        law = entry["LAW"]
        if law not in law_data:
            law_data[law] = {"QUESTIONS": [], "ANSWERS": []}
        law_data[law]["QUESTIONS"].extend(entry["QUESTIONS"])
        law_data[law]["ANSWERS"].extend(entry["ANSWERS"])
    return law_data

grouped_data_faqs = group_data_by_law_faqs(data_faqs)

@notmainBlueprint.route('/', methods=['GET'])
def index_faqs():
    return render_template('faqs.html', grouped_data_faqs=grouped_data_faqs)

@notmainBlueprint.route('/search_faqs', methods=['GET'])
def search_faqs():
    query = request.args.get('query')
    results = []

    if not query:
        return jsonify(data_faqs)

    for entry in data_faqs:
        if entry["LAW"] == query:
            results.append(entry)

    return jsonify(results)
