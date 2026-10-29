class Notification:
    class Message:
        __slots__ = "_hidden", "_string"
        middle_character_for_add = " "

        def __init__(self, string: str, hidden: bool = False) -> None:
            self._string, self._hidden = string, hidden

        def __add__(self, other: "Notification.Message | str"):
            assert isinstance(other, (str, Notification.Message))
            if isinstance(other, str):
                new_message = (self._string+other)
            else:
                new_message = f"{self}{Notification.Message.middle_character_for_add}{other}"

            return Notification.Message(new_message)

        def __str__(self):
            return "" if self._hidden else self._string

        def display(self):
            if self._hidden:
                return

            print(self._string)

    __slots__ = ()

    welcome = Message("Pygame system made by `lostsmile`")
    goodbye = Message("Bye bye!")
    init = Message("Initializing...")
    init_done = Message("Finished initializing")

    @classmethod
    def get_notification_message(cls, message_name: str):
        try:
            attr = getattr(cls, message_name)
            assert isinstance(attr, cls.Message)
        except AttributeError:
            raise ValueError(
                f"Message doesn't exist; use {cls.new_notification_message.__name__} to add {cls.Message.__name__}({message_name!r})")
        except AssertionError:
            raise ValueError(f"Not a valid message name: {message_name!r}")

        return attr

    @classmethod
    def display(cls, message_name: str):
        message_item = cls.get_notification_message(message_name)
        message_item.display()

    @classmethod
    def new_notification_message(cls, name: str, message: str, hidden: bool = False):
        new_messageItem = cls.Message(message, hidden)
        setattr(cls, name, new_messageItem)
        return new_messageItem


if __name__ == "__main__":
    def test0():
        Notification.new_notification_message("testing", "enabled test mode").display()
        Notification.display("testing")

    def test1():
        Notification.display(1)  # pyright: ignore[reportArgumentType]

    def test2():
        Notification.get_notification_message("__slots__")

    # Run each test independently so one error doesn't stop the others.
    for test in (test0, test1, test2):
        print(f"\nRunning {test.__name__}...")
        try:
            test()
        except Exception as e:
            print(f"Raised {type(e).__name__}: {e}")
        else:
            print("Completed without errors.")
