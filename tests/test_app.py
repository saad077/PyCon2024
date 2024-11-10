import os
import pytest
import time
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import app

# Helper function to clear logger handlers
def clear_logger_handlers():
    logger = app.logger
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)

@pytest.fixture(scope='function', autouse=True)
def clear_log_file():
    """Ensure the log file is cleaned up before and after tests."""
    yield  # Run the test
    clear_logger_handlers()

@pytest.fixture
def client():
    """Fixture to create a test client with TESTING and RUN_LOGS disabled."""
    app.config['TESTING'] = True
    app.config['RUN_LOGS'] = False  # Disable background logging
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Test that the home route returns the correct response."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Random log generator is running" in response.data

def test_log_file_creation():
    """Test that the log file is created and contains logs."""
    # Manually trigger log generation
    app.config['RUN_LOGS'] = True
    app.logger.debug("Test log entry")  # Simulate log generation

    assert os.path.exists('app.log')  # Check if log file exists

    # Read the log file and ensure it contains the log message
    with open('app.log', 'r') as log_file:
        log_content = log_file.read()
        assert "Test log entry" in log_content

def test_console_logging(caplog):
    """Test that logs are printed to the console."""
    with caplog.at_level('DEBUG'):
        app.logger.debug("Test console log")

        # Check if the log record is in the captured logs
        assert any("Test console log" in record.message for record in caplog.records)

def test_multiple_logs_generated():
    """Test that multiple logs are generated."""
    app.logger.debug("First log")
    app.logger.debug("Second log")

    with open('app.log', 'r') as log_file:
        log_content = log_file.readlines()
        assert len(log_content) >= 2  # Ensure multiple log lines are present
