import wx
import datetime
import timeline as tl


class InputWindow(wx.App):
    """
    InputWindow は、ユーザのマウスクリックを記録するためのウィンドウです。
    """
    def OnInit(self):
        self.init_frame()
        return True

    def OnClose(self, event):
        with open(self.file, 'w') as file:
            t: tl.TimelineEvent
            lastEvent: tl.TimelineEvent
            lastEvent = None
            framePos: wx.Point = self.frame.GetPosition()
            frameSize: wx.Size = self.frame.GetSize()
            file.write(f'Window:{framePos.x}:{framePos.y}:{frameSize.GetWidth()}:{frameSize.GetHeight()}\n')
            for t in self.timeline:
                if lastEvent is not None:
                    diff: datetime.datetime = t.time - lastEvent.time
                    file.write(f'{tl.TimelineEventType.SLEEP}:{diff.total_seconds()}\n')
                file.write(f'{t.kind}:{t.pos}\n')
                lastEvent = t
        self.frame.Destroy()

    def OnMouseLeftDown(self, event):
        pos = event.GetPosition()
        self.timeline.append(tl.TimelineEvent(
            datetime.datetime.now(),
            tl.TimelineEventType.LEFT_DOWN,
            pos)
        )

    def OnMouseRightDown(self, event):
        pos = event.GetPosition()
        self.timeline.append(tl.TimelineEvent(
            datetime.datetime.now(),
            tl.TimelineEventType.RIGHT_DOWN,
            pos)
        )

    def OnMouseLeftUp(self, event):
        pos = event.GetPosition()
        self.timeline.append(tl.TimelineEvent(
            datetime.datetime.now(),
            tl.TimelineEventType.LEFT_UP,
            pos)
        )

    def OnMouseRightUp(self, event):
        pos = event.GetPosition()
        self.timeline.append(tl.TimelineEvent(
            datetime.datetime.now(),
            tl.TimelineEventType.RIGHT_UP,
            pos)
        )

    def OnMouseMove(self, event):
        pos = event.GetPosition()
        self.timeline.append(tl.TimelineEvent(
            datetime.datetime.now(),
            tl.TimelineEventType.MOVE,
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
        self.frame.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.frame.Show()

    @property
    def file(self) -> str:
        return self.__file

    @file.setter
    def file(self, f: str):
        self.__file = f
