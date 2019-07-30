from datetime import timedelta
from multiprocessing.dummy import Pool as ThreadPool
import itertools
import numpy
from jinja2 import FileSystemLoader, Environment


def repeat_function_for_daterange(function, parameters, start_date, end_date, nr_threads=10):
    dates = numpy.array_split(get_dates_for_daterange(start_date, end_date),
                              nr_threads)
    with ThreadPool(nr_threads) as pool:
        pool.starmap(repeat_function_for_dates,
                     zip(itertools.repeat(function),
                         itertools.repeat(parameters),
                         dates)
                     )


def get_dates_for_daterange(start_date, end_date):
    return [(start_date + timedelta(i)) for i in range((end_date - start_date).days + 1)]


def repeat_function_for_dates(function, parameters, dates):
    for date in dates:
        run_function_for_date(function, parameters, date)


def run_function_for_date(function, parameters, date):
    parameters['date_suffix'] = get_suffix_from_date(date)
    try:
        function(**parameters)
    except Exception as e:
        print(f'Error for {function.__name__}: {e}')


def get_suffix_from_date(date):
    return f'{date.year}{date.month:02d}{date.day:02d}'


def get_query(file_name, params):
    templateEnv = Environment(
        loader=FileSystemLoader(searchpath='./sql_template'))
    template = templateEnv.get_template(file_name)
    return template.render(params)
