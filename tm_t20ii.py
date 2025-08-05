import serial

class Printer:
    def __init__(self, port: str, baud: int = 38400, start_connected: bool = True):
        self.port = port
        self.baud = baud
        self.conn = None
        if start_connected:
            self.connect()

    def _write(self, data: list[int]) -> bool:
        if not self.is_connected():
            return False
        write_retval = self.conn.write(bytearray(data))
        if write_retval is None or (len(write_retval) == 0 and len(data) != 0):
            return False
        return True

    def is_connected(self) -> bool:
        return self.conn is not None

    def connect(self) -> bool:
        already_connected = self.is_connected()
        if not already_connected:
            self.conn = serial.Serial(self.port, self.baud)
        return already_connected

    def disconnect(self) -> bool:
        was_connected = self.is_connected()
        if was_connected:
            self.conn.close()
            self.conn = None
        return was_connected