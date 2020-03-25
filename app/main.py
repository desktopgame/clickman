import pyautogui
import argparse
import wx


class InputWindow(wx.App):
    """
    InputWindow は、ユーザのマウスクリックを記録するためのウィンドウです。
    """
    def OnInit(self):
        self.init_frame()
        return True

    def OnMouseLeftDown(self, event):
        pos = event.GetPosition()
        self.frame.SetTitle('OnMouseLeftDown' + str(pos))

    def OnMouseRightDown(self, event):
        pos = event.GetPosition()
        self.frame.SetTitle('OnMouseRightDown' + str(pos))

    def OnMouseLeftUp(self, event):
        pos = event.GetPosition()
        self.frame.SetTitle('OnMouseLeftUp' + str(pos))

    def OnMouseRightUp(self, event):
        pos = event.GetPosition()
        self.frame.SetTitle('OnMouseRightUp' + str(pos))

    def init_frame(self):
        self.frame = wx.Frame(None)
        self.frame.SetTitle("Hello, wxPython!")
        self.frame.SetSize((800, 600))
        self.frame.SetPosition((0, 0))
        # コールバックの登録
        self.frame.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.frame.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.frame.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.frame.Bind(wx.EVT_RIGHT_UP, self.OnMouseRightUp)
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
