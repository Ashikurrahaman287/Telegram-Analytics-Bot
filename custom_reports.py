import os
import json
from datetime import datetime


class CustomReports:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.message_data_file = os.path.join(data_dir, 'message_data.json')
        self.load_message_data()

    def load_message_data(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        if os.path.exists(self.message_data_file):
            with open(self.message_data_file, 'r') as f:
                self.message_data = json.load(f)
        else:
            self.message_data = {}

    def generate_report(self, chat_id, start_date=None, end_date=None):
        if chat_id not in self.message_data:
            return "No data available for this chat."

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

        report = {}
        for user_id, messages in self.message_data[chat_id].items():
            user_messages = []
            for message in messages:
                timestamp = datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S')
                if (not start_date or timestamp >= start_date) and (not end_date or timestamp <= end_date):
                    user_messages.append(message)
            if user_messages:
                report[user_id] = user_messages

        return report


# Example usage:
if __name__ == "__main__":
    reports = CustomReports()

    # Generate report for a specific chat
    chat_id = 123456789
    report = reports.generate_report(chat_id)
    print("Report for Chat", chat_id)
    print(json.dumps(report, indent=4))

    # Generate report for a specific chat within a date range
    start_date = '2024-01-01'
    end_date = '2024-03-31'
    report_date_range = reports.generate_report(chat_id, start_date, end_date)
    print("\nReport for Chat", chat_id, "within date range:", start_date, "-", end_date)
    print(json.dumps(report_date_range, indent=4))
