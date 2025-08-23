from enum import Enum, auto
from typing import Type

import serial


class RTSFlags(Enum):
    _FLAG_BIT_POSITIONS = (2, 3, 5, 6)

    @staticmethod
    def _generate_next_value(name, start, count, last_values):
        RTSFlags._FLAG_BIT_POSITIONS[len(last_values)]


class RTSCommand:
    def __init__(self, n: int, a: int|None, resp_flag_enum: Type[RTSFlags]):
        self.n = n
        self.a = a
        self.resp_flag_enum = resp_flag_enum


class PrinterFlags(RTSFlags):
    DRAWER_KICK_OUT_CONNECTOR_PIN_3 = auto()
    OFFLINE = auto()
    WAITING_ONLINE_RECOVERY = auto()
    PAPER_FEED_BUTTON_PRESSED = auto()


class OfflineCauseFlags(RTSFlags):
    COVER_OPEN = auto()
    PAPER_FED_BY_BUTTON = auto()
    PRINTING_STOP_PAPER_END = auto()
    ERROR = auto()


class ErrorCauseFlags(RTSFlags):
    RECOVERABLE_ERROR = auto()
    AUTOCUTTER_ERROR = auto()
    UNRECOVERABLE_ERROR = auto()
    AUTO_RECOVERABLE_ERROR = auto()


class RollPaperSensorFlags(RTSFlags):
    # Ignoring redundant bits 3 and 6
    ROLL_PAPER_NEAR_END = 2
    ROLL_PAPER_END = 5


class InkFlags(RTSFlags):
    INK_NEAR_END_DETECTED = auto()
    INK_END_DETECTED = auto()
    INK_NOT_DETECTED = auto()
    CLEANING_BEING_PERFORMED = auto()


class PeelerFlags(RTSFlags):
    WAITING_FOR_LABEL_REMOVAL = 2
    NO_PAPER_IN_LABEL_PEELER = 5


class InterfaceFlags(RTSFlags):
    PRINTING_USING_MULTIPLE_IFACES_ENABLED = 2

class DMDFlags(RTSFlags):
    DM_D_TX_STATUS_BUSY = 2


class RTSType(Enum):
    PRINTER = RTSCommand(1, None, PrinterFlags)
    OFFLINE_CAUSE = RTSCommand(2, None, OfflineCauseFlags)
    ERROR_CAUSE = RTSCommand(3, None, ErrorCauseFlags)
    ROLL_PAPER_SENSOR = RTSCommand(4, None, RollPaperSensorFlags)
    INK_A = RTSCommand(7, 1, InkFlags)
    INK_B = RTSCommand(7, 2, InkFlags)
    PEELER = RTSCommand(8, 3, PeelerFlags)
    INTERFACE = RTSCommand(18, 1, InterfaceFlags)
    DM_D = RTSCommand(18, 2, DMDFlags)


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
    
    def realtime_status(self, status_type: RTSType) -> list[RTSFlags]:
        """DLE EOT: Transmit real-time status"""
        command = [16, 4, status_type.n]
        if status_type.a is not None:
            command.append(status_type.a)
        self.write(command)
        response = self.read()
        type_flags = status_type.value.resp_flag_enum.__members__.values()
        response_flags = [flag for flag in type_flags if response & (1 << flag.value)]
        return response_flags
