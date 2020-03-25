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


def fixstr(s: str):
    if s[0] == '(':
        return s[1:]
    elif s[len(s)-1] == ')':
        return s[0:len(s)-1]
    return s


def pairtopos(pos: list) -> wx.Point:
    return wx.Point((
        int(fixstr(pos[0])),
        int(fixstr(pos[1])))
    )


def parse(file: str) -> (wx.Point, wx.Size, list):
    dest = []
    pt = None
    si = None
    with open(file, 'r') as file:
        for line in file:
            line = line.strip()
            args = line.split(':')[1:]
            if line.startswith('Window'):
                pt = wx.Point(int(args[0]), int(args[1]))
                si = wx.Size(int(args[2]), int(args[3]))
            elif line.startswith(TimelineEventType.MOVE):
                pos = args[0].split(',')
                dest.append(TimelineEvent(
                    None,
                    TimelineEventType.LEFT_DOWN,
                    pairtopos(pos),
                    0
                ))
            elif line.startswith(TimelineEventType.SLEEP):
                dest.append(TimelineEvent(
                    None,
                    TimelineEventType.SLEEP,
                    None,
                    float(args[0])
                ))
            elif line.startswith(TimelineEventType.LEFT_DOWN):
                pos = args[0].split(',')
                dest.append(TimelineEvent(
                    None,
                    TimelineEventType.LEFT_DOWN,
                    pairtopos(pos),
                    0
                ))
            elif line.startswith(TimelineEventType.RIGHT_DOWN):
                dest.append(TimelineEvent(
                    None,
                    TimelineEventType.RIGHT_DOWN,
                    pairtopos(pos),
                    0
                ))
            elif line.startswith(TimelineEventType.LEFT_UP):
                dest.append(TimelineEvent(
                    None,
                    TimelineEventType.LEFT_UP,
                    pairtopos(pos),
                    0
                ))
            elif line.startswith(TimelineEventType.RIGHT_UP):
                dest.append(TimelineEvent(
                    None,
                    TimelineEventType.RIGHT_UP,
                    pairtopos(pos),
                    0
                ))
        return (pt, si, dest)
