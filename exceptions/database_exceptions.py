class ConnectionIsNull(Exception):
    def __init__(self) -> None:
        super().__init__("please, call db.connect() method before")