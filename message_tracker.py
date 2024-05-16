import os
import json
from datetime import datetime


class MessageTracker:
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

    def save_message_data(self):
        with open(self.message_data_file, 'w') as f:
            json.dump(self.message_data, f, indent=4)

    def track_message(self, chat_id, user_id, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if chat_id not in self.message_data:
            self.message_data[chat_id] = {}
        if user_id not in self.message_data[chat_id]:
            self.message_data[chat_id][user_id] = []

        self.message_data[chat_id][user_id].append({
            'timestamp': timestamp,
            'message': message
        })

        self.save_message_data()

    def get_user_message_count(self, chat_id, user_id):
        if chat_id in self.message_data and user_id in self.message_data[chat_id]:
            return len(self.message_data[chat_id][user_id])
        return 0

    def get_chat_message_count(self, chat_id):
        if chat_id in self.message_data:
            total_messages = sum(len(messages) for messages in self.message_data[chat_id].values())
            return total_messages
        return 0

    def get_user_messages(self, chat_id, user_id):
        if chat_id in self.message_data and user_id in self.message_data[chat_id]:
            return self.message_data[chat_id][user_id]
        return []


# Example usage:
if __name__ == "__main__":
    message_tracker = MessageTracker()

    # Track a message
    message_tracker.track_message(chat_id=123456789, user_id=987654321, message="Hello, world!")

    # Get user's message count
    user_message_count = message_tracker.get_user_message_count(chat_id=123456789, user_id=987654321)
    print(f"User message count: {user_message_count}")

    # Get total message count in chat
    chat_message_count = message_tracker.get_chat_message_count(chat_id=123456789)
    print(f"Total message count in chat: {chat_message_count}")

    # Get user's messages
    user_messages = message_tracker.get_user_messages(chat_id=123456789, user_id=987654321)
    print("User messages:")
    for msg in user_messages:
        print(f"{msg['timestamp']}: {msg['message']}")
