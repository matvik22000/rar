from eschool.eschool_interfaces import EschoolUserInterface


class UserInterface(EschoolUserInterface):
    def send_msgs(self) -> None: ...

    def get_firebase_id(self) -> str: ...
