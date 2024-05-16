import os
import json
from collections import defaultdict
from datetime import datetime


class UserActivityAnalyzer:
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

    def calculate_user_activity(self, chat_id):
        user_activity = defaultdict(int)

        if chat_id in self.message_data:
            for user_id, messages in self.message_data[chat_id].items():
                user_activity[user_id] = len(messages)

        return user_activity

    def calculate_user_engagement(self, chat_id):
        user_engagement = defaultdict(float)
        total_messages = self.get_chat_message_count(chat_id)

        if total_messages > 0:
            for user_id, messages in self.message_data[chat_id].items():
                user_engagement[user_id] = len(messages) / total_messages

        return user_engagement

    def get_chat_message_count(self, chat_id):
        if chat_id in self.message_data:
            total_messages = sum(len(messages) for messages in self.message_data[chat_id].values())
            return total_messages
        return 0


# Example usage:
if __name__ == "__main__":
    analyzer = UserActivityAnalyzer()

    # Calculate user activity
    chat_id = 123456789
    user_activity = analyzer.calculate_user_activity(chat_id)
    print("User Activity:")
    for user_id, activity in user_activity.items():
        print(f"User {user_id}: {activity} messages")

    # Calculate user engagement
    user_engagement = analyzer.calculate_user_engagement(chat_id)
    print("\nUser Engagement:")
    for user_id, engagement in user_engagement.items():
        print(f"User {user_id}: {engagement * 100:.2f}%")
