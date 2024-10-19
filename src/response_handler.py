# response_handler.py

import threading
import csv
import os

class ResponseHandler:
    lock = threading.Lock()
    file_name = 'results.csv'
    header_written = False

    @classmethod
    def save_response(cls, vusers_number, url, start_time, end_time, response_time_ms):
        with cls.lock:
            if not cls.header_written:
                with open(cls.file_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['VusersNumber', 'URL', 'StartTime', 'EndTime', 'ResponseTime[ms]'])
                cls.header_written = True

            with open(cls.file_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    vusers_number,
                    url,
                    start_time,
                    end_time,
                    f"{response_time_ms:.2f}"
                ])
