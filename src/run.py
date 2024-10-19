# run.py

from scenario import Scenario
from response_handler import ResponseHandler
import threading
import time
import requests
from datetime import datetime
from graph import generate_graph

# Define steps
step1 = Scenario("First URL").set_url("http://httpbin.org/get").set_method("GET").set_headers("").save("X-Amzn-Trace-Id")
step2 = Scenario("Second URL").set_url("http://httpbin.org/post").set_method("POST").set_headers("").set_body("X-Amzn-Trace-Id: {X-Amzn-Trace-Id}")
step3 = Scenario("Third URL").set_url("http://httpbin.org/put").set_method("PUT").set_headers("")

# Thread-local storage for variables
thread_local = threading.local()

class Run:
    @staticmethod
    def speed(vusers_number, duration):
        threads = []
        for _ in range(vusers_number):
            t = threading.Thread(target=Run.user_thread, args=(vusers_number, duration))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    @staticmethod
    def user_thread(vusers_number, duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            for step in [step1, step2, step3]:
                Run.execute_step(step, vusers_number)

    @staticmethod
    def execute_step(step, vusers_number):
        global thread_local
        if not hasattr(thread_local, 'variables'):
            thread_local.variables = {}

        # Handle variables in body
        body = step.body
        if body:
            for var_name, var_value in thread_local.variables.items():
                placeholder = "{" + var_name + "}"
                body = body.replace(placeholder, var_value)

        # Print request details
        print(f"Request to {step.url} with method {step.method}, headers {step.headers}, body {body}")

        # Send request
        request_start_time = datetime.now()
        start_timestamp = request_start_time.strftime('%Y-%m-%d-%H:%M:%S.%f')[:-4]
        try:
            response = requests.request(step.method, step.url, headers=step.headers, data=body)
            response_time_ms = round((datetime.now() - request_start_time).total_seconds() * 1000, 2)
            end_timestamp = datetime.now().strftime('%Y-%m-%d-%H:%M:%S.%f')[:-4]

            # Print response
            print(f"Response: {response.text}")

            # Save variable from response headers if needed
            if step.save_variable:
                var_value = response.headers.get(step.save_variable)
                if var_value:
                    thread_local.variables[step.save_variable] = var_value

            # Save response time
            ResponseHandler.save_response(vusers_number, step.url, start_timestamp, end_timestamp, response_time_ms)
        except Exception as e:
            print(f"Error during request: {e}")

if __name__ == '__main__':
    # Run performance tests
    Run.speed(1, 10)
    Run.speed(2, 5)

    # Generate graph after tests
    generate_graph()
