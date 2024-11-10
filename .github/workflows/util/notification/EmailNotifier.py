import smtplib
from email.mime.text import MIMEText
from Observer import Observer, logger


class EmailNotifier(Observer):
    def __init__(self, sender, smtp_server, smtp_port, recipient):
        self.sender = sender
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.recipient = recipient
    
    def update(self, message: str):
        """Send an email notification."""
        self.send_email(message)
    
    def send_email(self, message: str):
        msg = MIMEText(message)
        msg['Subject'] = 'Notification Alert'
        msg['From'] = self.sender
        msg['To'] = self.recipient

        # Replace with your SMTP configuration
        try:
            timeout = 60
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=timeout) as server:
                server.sendmail(self.sender, self.recipient, msg.as_string())  # Use msg.as_string()
            logger.info("Email sent successfully!")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")  # Corrected logging format

