import serial


import realtime


class Printer:
    def __init__(self, port: str, baud: int = 38400, start_connected: bool = True):
        """
        TODO: finish this documentation
        Reference: https://download4.epson.biz/sec_pubs/pos/reference_en/escpos/tmt20ii.html
        """
        self.port = port
        self.baud = baud
        self.conn = None
        if start_connected:
            self.connect()

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
    
    def read(self) -> bytes|bool:
        return self.conn.read_all() if self.is_connected() else False
    
    def write(self, data: list[int]) -> bool:
        if not self.is_connected():
            return False
        write_retval = self.conn.write(bytearray(data))
        if write_retval is None or (len(write_retval) == 0 and len(data) != 0):
            return False
        return True
    
    def print(self, text: str) -> bool:
        if not isinstance(text, str):
            return False
        return self.write(text.encode('ascii'))
    
    def horizontal_tab(self) -> bool:
        """HT: Horizontal tab"""
        return self.write([9])
    
    def line_feed(self) -> bool:
        """LF: Print and line feed"""
        return self.write([10])
    
    def ff(self) -> bool:
        """FF: Print and return to Standard mode (in Page mode)"""
        return self.write([12])
    
    def carriage_return(self) -> bool:
        """CR: Print and carriage return"""
        return self.write([13])
    
    def realtime_status(self, status_type: realtime.RTSType) -> list[realtime.RTSFlags]:
        """DLE EOT: Transmit real-time status"""
        command = [16, 4, status_type.n]
        if status_type.a is not None:
            command.append(status_type.a)
        self.write(command)
        response = self.read()
        type_flags = status_type.value.resp_flag_enum.__members__.values()
        response_flags = [flag for flag in type_flags if response & (1 << flag.value)]
        return response_flags
