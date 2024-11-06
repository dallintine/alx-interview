#!/usr/bin/python3
'''A script for parsing HTTP request logs and computing metrics.'''
import re
import sys

def extract_input(input_line):
    '''Extracts sections of a line of an HTTP request log.'''
    fp = (
        r'\s*(?P<ip>\S+)\s*',
        r'\s*\[(?P<date>[^\]]+)\]',
        r'\s*"(?P<request>[^"]*)"\s*',
        r'\s*(?P<status_code>\d+)',
        r'\s*(?P<file_size>\d+)'
    )
    log_fmt = '{}\\-{}{}{}{}\\s*'.format(fp[0], fp[1], fp[2], fp[3], fp[4])
    resp_match = re.fullmatch(log_fmt, input_line)
    if resp_match:
        return {
            'status_code': resp_match.group('status_code'),
            'file_size': int(resp_match.group('file_size'))
        }
    return None

def print_statistics(total_file_size, status_codes_stats):
    '''Prints the accumulated statistics of the HTTP request log.'''
    print('File size: {:d}'.format(total_file_size), flush=True)
    for status_code in sorted(status_codes_stats.keys()):
        if status_codes_stats[status_code] > 0:
            print('{:s}: {:d}'.format(status_code, status_codes_stats[status_code]), flush=True)

def run():
    '''Starts the log parser.'''
    line_num = 0
    total_file_size = 0
    status_codes_stats = {str(code): 0 for code in [200, 301, 400, 401, 403, 404, 405, 500]}

    try:
        for line in sys.stdin:
            line_info = extract_input(line.strip())
            if line_info:
                total_file_size += line_info['file_size']
                status_code = line_info['status_code']
                if status_code in status_codes_stats:
                    status_codes_stats[status_code] += 1
                line_num += 1
                if line_num % 10 == 0:
                    print_statistics(total_file_size, status_codes_stats)
    except KeyboardInterrupt:
        pass
    finally:
        print_statistics(total_file_size, status_codes_stats)

if __name__ == '__main__':
    run()

