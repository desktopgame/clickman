import pyautogui
import argparse
import wx
import datetime


class TimelineEventType:
    LEFT_DOWN = "LeftDown"
    RIGHT_DOWN = "RightDown"
    LEFT_UP = "LeftUp"
    RIGHT_UP = "RightUp"


class TimelineEvent:
    def __init__(self, time: datetime.datetime, kind: str, pos: wx.Point):
        self.__time = time
        self.__kind = kind
        self.__pos = pos

    @property
    def time(self) -> datetime.datetime:
        return self.__time

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def pos(self) -> wx.Point:
        return self.__pos


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
            for t in self.timeline:
                file.write(f'{t.kind}:{t.pos}\n')
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


def cmd_setup(args):
    app = InputWindow(False)
    app.MainLoop()


def cmd_test(args):
    pass


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
