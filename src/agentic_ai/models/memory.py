
class Memory:
    def __init__(self):
        self.history = []
        self.user_chat_history = []
        self.ai_chat_history = []

    def reset(self):
        self.history = []
        self.user_chat_history = []
        self.ai_chat_history = []
