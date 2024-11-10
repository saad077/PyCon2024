from flask import Flask
import logging
import random
import time
from threading import Thread

app = Flask(__name__)

# Set up logging to both file and console
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# File handler for logging to a file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Stream handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Random log levels and messages
log_levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL]
log_messages = [
    "Processing data...",
    "User logged in.",
    "File uploaded successfully.",
    "Data validation failed."
]

def generate_random_log():
    """Generate a random log message at a random log level."""
    level = random.choice(log_levels)
    message = random.choice(log_messages)

    # Log the message
    logging.log(level, message)

def log_generator():
    """Continuously generate random logs every 5 seconds, and log any exceptions that occur."""
    time_cal = 0
    while True:
        try:
            generate_random_log()
            time.sleep(5)  
            time_cal += 1
            if time_cal > 25:
                raise Exception('Exception occured due after the log generation is overlimit') 
        except Exception as e:
            # Log the exception with traceback
            logger.exception("An exception occurred during log generation")

# Run log generator in a separate thread
log_thread = Thread(target=log_generator)
log_thread.daemon = True  # This makes sure the thread stops when the main program exits
log_thread.start()

@app.route('/')
def home():
    return "Random log generator is running. Check the app.log file and console for continuous logs."

if __name__ == '__main__':
    app.run(debug=True)
