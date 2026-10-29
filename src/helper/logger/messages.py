
class show_message:
    __slots__ = "Message"

    def __init__(self, Message: str):
        self.Message = Message

    def __str__(self):
        return self.Message
