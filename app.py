from flask import Flask, render_template, request, flash
from bq_toolbelt import copy_table, delete_table, write_query_result
from helper import repeat_function_for_daterange
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def _get_jobs():
    return [dict(zip(list(request.form.keys()), values_list))
            for values_list in [list(values) for values in zip(*request.form.listvalues())]]


@app.route("/", methods=['POST', 'GET'])
@app.route("/copy", methods=['POST', 'GET'])
def copy():
    if request.method == 'POST':
        for job in _get_jobs():
            repeat_function_for_daterange(function=copy_table,
                                          parameters={'source_project': job['source_project'],
                                                      'source_dataset': job['source_dataset'],
                                                      'source_table': job['source_table'],
                                                      'dest_project': job['destination_project'],
                                                      'dest_dataset': job['destination_dataset'],
                                                      'dest_table': job['destination_table']},
                                          start_date=datetime.strptime(
                                              job['start_date'], '%Y/%m/%d'),
                                          end_date=datetime.strptime(job['end_date'], '%Y/%m/%d'))

        flash(_get_jobs())
    return render_template('copy.html')


@app.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        for job in _get_jobs():
            repeat_function_for_daterange(function=delete_table,
                                          parameters={'project': job['project'],
                                                      'dataset': job['dataset'],
                                                      'table': job['table']},
                                          start_date=datetime.strptime(
                                              job['start_date'], '%Y/%m/%d'),
                                          end_date=datetime.strptime(job['end_date'], '%Y/%m/%d'))
        flash(_get_jobs())
    return render_template('delete.html')


@app.route("/write", methods=['POST', 'GET'])
def write():
    if request.method == 'POST':
        files = (file for file in request.files.getlist('sql_file'))
        for job in _get_jobs():
            next(files).save(os.path.join(
                './sql_template', 'sql_template.sql'))
            repeat_function_for_daterange(function=write_query_result,
                                          parameters={'project': job['project'],
                                                      'dataset': job['dataset'],
                                                      'table': job['table'],
                                                      'sql_filename': 'sql_template.sql',
                                                      'write_disposition': job['write_disposition']},
                                          start_date=datetime.strptime(
                                              job['start_date'], '%Y/%m/%d'),
                                          end_date=datetime.strptime(job['end_date'], '%Y/%m/%d'))
        filenames = (f.filename for f in request.files.getlist('sql_file'))
        flash([{**job, 'sql_file': next(filenames)} for job in _get_jobs()])
    return render_template('write.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
