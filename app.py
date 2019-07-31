from flask import Flask, render_template, request, flash
from bq_toolbelt import copy_table, delete_table, write_query_result
from helper import repeat_function_for_daterange
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
@app.route("/copy", methods=['POST', 'GET'])
def copy():
    if request.method == 'POST':
        repeat_function_for_daterange(function=copy_table,
                                      parameters={'source_project': request.form['source_project'],
                                                  'source_dataset': request.form['source_dataset'],
                                                  'source_table': request.form['source_table'],
                                                  'dest_project': request.form['destination_project'],
                                                  'dest_dataset': request.form['destination_dataset'],
                                                  'dest_table': request.form['destination_table']},
                                      start_date=datetime.strptime(
                                          request.form['start_date'], '%Y/%m/%d'),
                                      end_date=datetime.strptime(request.form['end_date'], '%Y/%m/%d'))
        flash(request.form)
    return render_template('copy.html')


@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        repeat_function_for_daterange(function=delete_table,
                                      parameters={'project': request.form['project'],
                                                  'dataset': request.form['dataset'],
                                                  'table': request.form['table']},
                                      start_date=datetime.strptime(
                                          request.form['start_date'], '%Y/%m/%d'),
                                      end_date=datetime.strptime(request.form['end_date'], '%Y/%m/%d'))
        flash(request.form)
    return render_template('delete.html')


@app.route("/write", methods=['POST', 'GET'])
def write():
    if request.method == 'POST':
        request.files['sql_file'].save(os.path.join(
            './sql_template', 'sql_template.sql'))
        repeat_function_for_daterange(function=write_query_result,
                                      parameters={'project': request.form['project'],
                                                  'dataset': request.form['dataset'],
                                                  'table': request.form['table'],
                                                  'sql_filename': 'sql_template.sql',
                                                  'write_disposition': request.form['write_disposition']},
                                      start_date=datetime.strptime(
                                          request.form['start_date'], '%Y/%m/%d'),
                                      end_date=datetime.strptime(request.form['end_date'], '%Y/%m/%d'))
        flash({**request.form, 'sql_file': request.files['sql_file'].filename})
    return render_template('write.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
