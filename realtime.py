from enum import Enum, auto
from typing import Type


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