import argparse
import os.path as osp
import os
import csv
import time
from loguru import logger
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--link", type=str, help="Link to html page for analysis", required=True)
    parser.add_argument("-o", "--output_file", type=str, default="statistic", help="Output file with statistic")
    args = parser.parse_args()
    return args


def timeit(f):
    """Measures time of function execution"""
    def wrap(*args):
        time1 = time.time()
        result = f(*args)
        time2 = time.time()
        work_time = round(time2 - time1, 3)
        logger.info(f"Function: <{f.__name__}> worked {work_time} seconds")
        return result, work_time

    return wrap


def dump_results_to_csv(output_name, results):
    path = f"{output_name}.csv"
    if isinstance(results, list):
        with open(path, "w") as file:
            writer = csv.writer(file)
            writer.writerows(results)
    elif isinstance(results, dict) or isinstance(results, defaultdict):
        csv_columns = results.keys()
        try:
            with open(path, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in results:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
