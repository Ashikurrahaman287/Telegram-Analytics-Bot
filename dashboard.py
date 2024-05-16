import os
import json
from collections import Counter


class Dashboard:
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

    def get_user_message_count(self, chat_id, user_id):
        if chat_id in self.message_data and user_id in self.message_data[chat_id]:
            return len(self.message_data[chat_id][user_id])
        return 0

    def get_chat_message_count(self, chat_id):
        if chat_id in self.message_data:
            total_messages = sum(len(messages) for messages in self.message_data[chat_id].values())
            return total_messages
        return 0

    def get_most_active_users(self, chat_id, num_users=5):
        user_activity = Counter()

        if chat_id in self.message_data:
            for user_id, messages in self.message_data[chat_id].items():
                user_activity[user_id] = len(messages)

        return user_activity.most_common(num_users)

    def get_top_topics(self, chat_id, num_topics=5):
        topics = Counter()

        if chat_id in self.message_data:
            for messages in self.message_data[chat_id].values():
                for message in messages:
                    topics.update(message['message'].split())

        return topics.most_common(num_topics)


# Example usage:
if __name__ == "__main__":
    dashboard = Dashboard()

    # Get user message count
    chat_id = 123456789
    user_id = 987654321
    user_message_count = dashboard.get_user_message_count(chat_id, user_id)
    print(f"User {user_id} message count: {user_message_count}")

    # Get chat message count
    chat_message_count = dashboard.get_chat_message_count(chat_id)
    print(f"Total message count in chat: {chat_message_count}")

    # Get most active users
    num_users = 5
    most_active_users = dashboard.get_most_active_users(chat_id, num_users)
    print("Most Active Users:")
    for user_id, message_count in most_active_users:
        print(f"User {user_id}: {message_count} messages")

    # Get top topics
    num_topics = 5
    top_topics = dashboard.get_top_topics(chat_id, num_topics)
    print("\nTop Topics:")
    for topic, count in top_topics:
        print(f"{topic}: {count} occurrences")
