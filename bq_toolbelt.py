from google.cloud import bigquery
from datetime import datetime
from helper import get_query


client = bigquery.Client.from_service_account_json(
    'bq_service_account/bq_service_account.json')


def copy_table(date_suffix, source_project, source_dataset, source_table,
               dest_project, dest_dataset, dest_table):
    source_table += date_suffix
    dest_table += date_suffix
    source_table_ref = client.dataset(
        source_dataset, project=source_project).table(source_table)
    dest_table_ref = client.dataset(
        dest_dataset, project=dest_project).table(dest_table)
    job = client.copy_table(
        source_table_ref,
        dest_table_ref,
        location='US')
    print(f'Send copy job for {source_project}.{source_dataset}.{source_table} to {dest_project}.{dest_dataset}.{dest_table} \n')


def delete_table(date_suffix, project, dataset, table):
    table += date_suffix
    table_ref = client.dataset(dataset, project=project).table(table)
    client.delete_table(table_ref)
    print(f'Send delete job for {project}.{dataset}.{table} \n')


def write_query_result(date_suffix, sql_filename, project, dataset, table, write_disposition):
    if write_disposition == 'WRITE_APPEND_ONE':
        write_disposition = 'WRITE_APPEND'
    else:
        table += date_suffix

    table_ref = client.dataset(
        dataset, project=project).table(table)
    job_config = bigquery.QueryJobConfig()
    job_config.destination = table_ref
    job_config.write_disposition = write_disposition
    query_job = client.query(get_query(sql_filename,
                                       params={'date': date_suffix}), job_config=job_config)
    query_job.result()
    print(f'Query written to table: {project}.{dataset}.{table} \n')
