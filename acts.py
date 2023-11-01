from flask import Flask, render_template, request, jsonify,Blueprint
from google.oauth2 import service_account
import gspread

actspage = Blueprint("actspage",__name__, template_folder="templates")


credentials = service_account.Credentials.from_service_account_file(
    "static/data/indian-legal-information-d6444bb36676.json",
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)


spreadsheet_id = '1TF1wNhRZVw33KHBWDG_FWekf9V2QOvdD5oWfmLRYhrI'

client = gspread.authorize(credentials)
worksheet = client.open_by_key(spreadsheet_id).sheet1

def get_ministries():
    all_data = worksheet.get_all_values()
    header = all_data[0]
    ministry_column_index = header.index('Ministry')  
    ministries = set(row[ministry_column_index] for row in all_data[1:])
    return list(ministries)

def get_filtered_and_paginated_data(selected_ministry, act_number, page, rows_per_page):
    all_data = worksheet.get_all_values()
    header = all_data[0]
    data = all_data[1:]

    if selected_ministry:
        ministry_column_index = header.index('Ministry') 
        data = [row for row in data if row[ministry_column_index] == selected_ministry]

    if act_number:
        act_number_column_index = header.index('Act_Number') 
        data = [row for row in data if row[act_number_column_index] == act_number]

    page = int(page)  

    if rows_per_page == 'all':
        paginated_data = data  
    else:
        rows_per_page = int(rows_per_page)  
        start_row = (page - 1) * rows_per_page
        end_row = start_row + rows_per_page
        paginated_data = data[start_row:end_row]

    return paginated_data

@actspage.route('/')
def Lawandregulations():
    ministries = get_ministries()
    selected_ministry = request.args.get('ministry', '') 
    total_rows = len(get_filtered_and_paginated_data(selected_ministry, '', 1, 'all')) 
    return render_template('Lawandregulations.html', ministries=ministries, total_rows=total_rows)

@actspage.route('/data', methods=['GET'])
def get_data():
    page = int(request.args.get('page', 1)) 
    selected_ministry = request.args.get('ministry', '')
    act_number = request.args.get('act_number', '') 
    rows_per_page = request.args.get('rows_per_page', 20)

    paginated_data = get_filtered_and_paginated_data(selected_ministry, act_number, page, rows_per_page)
    total_rows = len(get_filtered_and_paginated_data(selected_ministry, act_number, 1, 'all')) 

    total_pages = (total_rows + int(rows_per_page) - 1) // int(rows_per_page)

    return jsonify({'data': paginated_data, 'total_pages': total_pages})

