import wx
import datetime
import timeline as tl


class TestWindow(wx.App):
    """
    TestWindow は、ユーザの記録を再生するためのウィンドウです。
    """
    def OnInit(self):
        self.init_frame()
        return True

    def __draw_cross_point(self, dc: wx.AutoBufferedPaintDC, pos: wx.Point):
        size: wx.Size = self.frame.GetSize()
        dc.DrawLine(0, 0, pos.x, pos.y)
        dc.DrawLine(size.x, 0, pos.x, pos.y)
        dc.DrawLine(0, size.y, pos.x, pos.y)
        dc.DrawLine(size.x, size.y, pos.x, pos.y)

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self.frame)
        dc.Clear()
        if len(self.timeline) == 0:
            self.timer.Stop()
            self.frame.Destroy()
            return
        event = self.timeline[0]
        if event.kind == tl.TimelineEventType.LEFT_DOWN:
            dc.SetPen(wx.RED_PEN)
            self.__draw_cross_point(dc, event.pos)
            self.timeline.pop(0)
        elif event.kind == tl.TimelineEventType.RIGHT_DOWN:
            dc.SetPen(wx.RED_PEN)
            self.__draw_cross_point(dc, event.pos)
            self.timeline.pop(0)
        elif event.kind == tl.TimelineEventType.LEFT_UP:
            dc.SetPen(wx.BLUE_PEN)
            self.__draw_cross_point(dc, event.pos)
            self.timeline.pop(0)
        elif event.kind == tl.TimelineEventType.RIGHT_UP:
            dc.SetPen(wx.BLUE_PEN)
            self.__draw_cross_point(dc, event.pos)
            self.timeline.pop(0)
        elif event.kind == tl.TimelineEventType.MOVE:
            dc.DrawCircle(event.pos.x, event.pos.y, 2)
            self.timeline.pop(0)
        elif event.kind == tl.TimelineEventType.SLEEP:
            time: datetime.datetime = datetime.datetime.now()
            if self.time is None:
                self.time = datetime.datetime.now()
            if (time - self.time).total_seconds() > event.sleep:
                self.timeline.pop(0)
            else:
                return
        self.time = datetime.datetime.now()

    def OnClose(self, event):
        self.timer.Stop()
        self.Destroy()
        self.timer = None
        self.frame = None

    def OnTimer(self, event):
        if self.timer is not None and self.frame is not None:
            self.frame.Refresh()

    def init_frame(self):
        self.time = None
        self.frame = wx.Frame(None)
        self.frame.SetTitle("clickman")
        self.frame.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.timer = wx.Timer(self)
        self.timer.Start(1.0 / 60.0)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.frame.Bind(wx.EVT_PAINT, self.OnPaint)
        self.frame.Show()

    def load(self):
        pt, si, li = tl.parse(self.file)
        self.frame.SetPosition(pt)
        self.frame.SetSize(si)
        self.timeline = li

    @property
    def file(self) -> str:
        return self.__file

    @file.setter
    def file(self, f: str):
        self.__file = f

