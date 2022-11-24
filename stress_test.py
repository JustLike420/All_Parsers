# from threading import Thread
# import requests
#
# def main(url):
#     req = requests.get(url)
#     print(req.status_code)
#
#
# if __name__ == "__main__":
#     threads = 10
#     url = 'http://zoopt.ru'
#     for i in range(threads):
#         t = Thread(target=main, args=(url,))
#         t.start()
#         t.join(0.3)

import requests
import multiprocessing
from time import *


session = None


def global_requests_session():
    global session
    if not session:
        session = requests.Session()


def http_client_sessions_to_map(url):
    with session.get(url) as response:
        blank_var = response.status_code
        cpu_count = multiprocessing.cpu_count()
        print(f'Server CPU Count: {cpu_count} {blank_var}')


def http_client_multiprocessor_map(http_target_list):
    with multiprocessing.Pool(initializer=global_requests_session) as pool:
        pool.map(http_client_sessions_to_map, http_target_list)


if __name__ == "__main__":
    program_start_time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    http_target_list = [
                           "https://protuning.com/en/catalogue"
    ] * 334
    print(f'Started HTTP Stress Test @ {program_start_time}')
    start_time = time()
    http_client_multiprocessor_map(http_target_list)
    duration = time() - start_time
    program_stop_time = strftime("%a, %d %b %Y %H:%M:%S", localtime())
    print(f'Stopped HTTP Stress Test @ {program_stop_time}')
    total_targets = "{:,}".format(len(http_target_list))
    print(f'Sent {total_targets} HTTP GET Requests in {duration} seconds')