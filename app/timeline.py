import datetime
import wx


class TimelineEventType:
    LEFT_DOWN = "LeftDown"
    RIGHT_DOWN = "RightDown"
    LEFT_UP = "LeftUp"
    RIGHT_UP = "RightUp"
    MOVE = "Move"
    SLEEP = "Sleep"


class TimelineEvent:
    def __init__(
        self,
        time: datetime.datetime,
        kind: str, pos: wx.Point,
        sleep: float = 0
    ):
        self.__time = time
        self.__kind = kind
        self.__pos = pos
        self.__sleep = sleep

    @property
    def time(self) -> datetime.datetime:
        return self.__time

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def pos(self) -> wx.Point:
        return self.__pos

    @property
    def sleep(self) -> float:
        return self.__sleep
