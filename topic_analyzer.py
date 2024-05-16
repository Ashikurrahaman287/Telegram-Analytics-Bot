import os
import json
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string


class TopicAnalyzer:
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

    def analyze_topics(self, chat_id, num_topics=5):
        topics = Counter()

        if chat_id in self.message_data:
            for messages in self.message_data[chat_id].values():
                for message in messages:
                    topics.update(self.extract_topics(message['message']))

        return topics.most_common(num_topics)

    def extract_topics(self, message):
        # Tokenize the message
        tokens = word_tokenize(message.lower())

        # Remove punctuation and stopwords
        tokens = [token for token in tokens if
                  token not in string.punctuation and token not in stopwords.words('english')]

        # Lemmatize tokens
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

        return tokens


# Example usage:
if __name__ == "__main__":
    analyzer = TopicAnalyzer()

    # Analyze topics
    chat_id = 123456789
    top_topics = analyzer.analyze_topics(chat_id)
    print("Top Topics:")
    for topic, count in top_topics:
        print(f"{topic}: {count} occurrences")
