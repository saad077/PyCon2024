import argparse
from TeamsNotifier import TeamsNotifier
from EmailNotifier import EmailNotifier
from Manager import Manager

def main(sender, smtp_server, smtp_port, recipient, webhook, message):
    # Create the subject (Manager)
    notification_system = Manager()

    # Create the observers
    email_notifier = EmailNotifier(sender, smtp_server, smtp_port, recipient)
    teams_notifier = TeamsNotifier(webhook)

    # Attach observers
    notification_system.attach(email_notifier)
    notification_system.attach(teams_notifier)

    # Notify observers
    notification_system.notify(message)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Send notifications to email and Teams.")

    parser.add_argument("--sender", required=True, help="The sender email address.")
    parser.add_argument("--smtp_server", required=True, help="The SMTP server address.")
    parser.add_argument("--smtp_port", required=True, type=int, help="The SMTP server port.")
    parser.add_argument("--recipient", required=True, help="The email address to send notifications to.")
    parser.add_argument("--webhook", required=False, help="The webhook URL for Teams notifications.")
    parser.add_argument("--message", required=True, help="The notification message to send to different platforms")

    args = parser.parse_args()

    # Call the main function with parsed arguments
    main(args.sender, args.smtp_server, args.smtp_port, args.recipient, args.webhook, args.message)
