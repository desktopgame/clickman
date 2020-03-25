import pyautogui
import argparse
import wx
import datetime
import os


class TimelineEventType:
    LEFT_DOWN = "LeftDown"
    RIGHT_DOWN = "RightDown"
    LEFT_UP = "LeftUp"
    RIGHT_UP = "RightUp"


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


class InputWindow(wx.App):
    """
    InputWindow は、ユーザのマウスクリックを記録するためのウィンドウです。
    """
    def OnInit(self):
        self.init_frame()
        return True

    def OnClose(self, event):
        with open('clickman.txt', 'w') as file:
            t: TimelineEvent
            lastEvent: TimelineEvent
            lastEvent = None
            framePos: wx.Point = self.frame.GetPosition()
            frameSize: wx.Size = self.frame.GetSize()
            file.write(f'window:{framePos.x}:{framePos.y}:{frameSize.GetWidth()}:{frameSize.GetHeight()}\n')
            for t in self.timeline:
                if lastEvent is not None:
                    diff: datetime.datetime = t.time - lastEvent.time
                    file.write(f'sleep:{diff.total_seconds()}\n')
                file.write(f'{t.kind}:{t.pos}\n')
                lastEvent = t
        self.frame.Destroy()

    def OnMouseLeftDown(self, event):
        pos = event.GetPosition()
        self.timeline.append(TimelineEvent(
            datetime.datetime.now(),
            TimelineEventType.LEFT_DOWN,
            pos)
        )

    def OnMouseRightDown(self, event):
        pos = event.GetPosition()
        self.timeline.append(TimelineEvent(
            datetime.datetime.now(),
            TimelineEventType.RIGHT_DOWN,
            pos)
        )

    def OnMouseLeftUp(self, event):
        pos = event.GetPosition()
        self.timeline.append(TimelineEvent(
            datetime.datetime.now(),
            TimelineEventType.LEFT_UP,
            pos)
        )

    def OnMouseRightUp(self, event):
        pos = event.GetPosition()
        self.timeline.append(TimelineEvent(
            datetime.datetime.now(),
            TimelineEventType.RIGHT_UP,
            pos)
        )

    def init_frame(self):
        self.timeline = []
        self.frame = wx.Frame(None)
        self.frame.SetTitle("clickman")
        self.frame.SetSize((800, 600))
        self.frame.SetPosition((0, 0))
        # コールバックの登録
        self.frame.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.frame.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.frame.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.frame.Bind(wx.EVT_RIGHT_UP, self.OnMouseRightUp)
        self.frame.Bind(wx.EVT_CLOSE, self.OnClose)
        self.frame.Show()


class TestWindow(wx.App):
    """
    TestWindow は、ユーザの記録を再生するためのウィンドウです。
    """
    def OnInit(self):
        self.init_frame()
        return True

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self.frame)
        dc.Clear()
        if len(self.timeline) == 0:
            self.frame.Destroy()
            return
        event = self.timeline[0]
        if event.kind == TimelineEventType.LEFT_DOWN:
            dc.SetPen(wx.RED_PEN)
            dc.DrawLine(0, 0, event.pos.x, event.pos.y)
            self.timeline.pop(0)
        elif event.kind == TimelineEventType.RIGHT_DOWN:
            self.timeline.pop(0)
        elif event.kind == TimelineEventType.LEFT_UP:
            self.timeline.pop(0)
        elif event.kind == TimelineEventType.RIGHT_UP:
            self.timeline.pop(0)
        elif event.kind == 'sleep':
            time: datetime.datetime = datetime.datetime.now()
            if (time - self.time).total_seconds() > event.sleep:
                self.timeline.pop(0)
            else:
                return
        self.time = datetime.datetime.now()

    def OnClose(self, event):
        self.timer.Stop()
        self.Destroy()

    def OnTimer(self, event):
        self.frame.Refresh()

    @staticmethod
    def fixstr(s: str):
        if s[0] == '(':
            return s[1:]
        elif s[len(s)-1] == ')':
            return s[0:len(s)-1]
        return s

    @staticmethod
    def pairtopos(pos: list) -> wx.Point:
        return wx.Point((
            int(TestWindow.fixstr(pos[0])),
            int(TestWindow.fixstr(pos[1])))
        )

    def init_frame(self):
        self.timeline = []
        self.time = None
        self.frame = wx.Frame(None)
        self.frame.SetTitle("clickman")
        self.frame.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.timer = wx.Timer(self)
        self.timer.Start(1.0 / 60.0)
        with open('clickman.txt', 'r') as file:
            for line in file:
                line = line.strip()
                args = line.split(':')[1:]
                if line.startswith('window'):
                    self.frame.SetPosition((int(args[0]), int(args[1])))
                    self.frame.SetSize((int(args[2]), int(args[3])))
                elif line.startswith('sleep'):
                    self.timeline.append(TimelineEvent(
                        None,
                        'sleep',
                        None,
                        float(args[0])
                    ))
                elif line.startswith(TimelineEventType.LEFT_DOWN):
                    pos = args[0].split(',')
                    self.timeline.append(TimelineEvent(
                        None,
                        TimelineEventType.LEFT_DOWN,
                        TestWindow.pairtopos(pos),
                        0
                    ))
                elif line.startswith(TimelineEventType.RIGHT_DOWN):
                    self.timeline.append(TimelineEvent(
                        None,
                        TimelineEventType.RIGHT_DOWN,
                        TestWindow.pairtopos(pos),
                        0
                    ))
                elif line.startswith(TimelineEventType.LEFT_UP):
                    self.timeline.append(TimelineEvent(
                        None,
                        TimelineEventType.LEFT_UP,
                        TestWindow.pairtopos(pos),
                        0
                    ))
                elif line.startswith(TimelineEventType.RIGHT_UP):
                    self.timeline.append(TimelineEvent(
                        None,
                        TimelineEventType.RIGHT_UP,
                        TestWindow.pairtopos(pos),
                        0
                    ))
        self.frame.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.frame.Show()


def cmd_setup(args):
    app = InputWindow(False)
    app.MainLoop()


def cmd_test(args):
    if not os.path.exists("clickman.txt"):
        print('clickman.txt is not found')
        exit(1)
        return
    app = TestWindow(False)
    app.MainLoop()


parser: argparse.ArgumentParser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# `setup` コマンドの parser を作成
parser_setup = subparsers.add_parser('setup', help='see `setup -h`')
parser_setup.set_defaults(handler=cmd_setup)

# `test` コマンドの parser を作成
parser_test = subparsers.add_parser('test', help='see `test -h`')
parser_test.set_defaults(handler=cmd_test)

# コマンドの内容に関係なくインフォメーションを表示
screen_x, screen_y = pyautogui.size()
mouse_x, mouse_y = pyautogui.position()

print(f'screenX={screen_x} screenY={screen_y}')
print(f'mouseX={mouse_x} mouseY={mouse_y}')


# コマンドラインを解析して実行
args = parser.parse_args()
if hasattr(args, 'handler'):
    args.handler(args)
else:
    parser.print_help()
