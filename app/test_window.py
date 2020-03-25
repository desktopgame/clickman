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
                if line.startswith('Window'):
                    self.frame.SetPosition((int(args[0]), int(args[1])))
                    self.frame.SetSize((int(args[2]), int(args[3])))
                elif line.startswith(tl.TimelineEventType.MOVE):
                    pos = args[0].split(',')
                    self.timeline.append(tl.TimelineEvent(
                        None,
                        tl.TimelineEventType.LEFT_DOWN,
                        TestWindow.pairtopos(pos),
                        0
                    ))
                elif line.startswith(tl.TimelineEventType.SLEEP):
                    self.timeline.append(tl.TimelineEvent(
                        None,
                        tl.TimelineEventType.SLEEP,
                        None,
                        float(args[0])
                    ))
                elif line.startswith(tl.TimelineEventType.LEFT_DOWN):
                    pos = args[0].split(',')
                    self.timeline.append(tl.TimelineEvent(
                        None,
                        tl.TimelineEventType.LEFT_DOWN,
                        TestWindow.pairtopos(pos),
                        0
                    ))
                elif line.startswith(tl.TimelineEventType.RIGHT_DOWN):
                    self.timeline.append(tl.TimelineEvent(
                        None,
                        tl.TimelineEventType.RIGHT_DOWN,
                        TestWindow.pairtopos(pos),
                        0
                    ))
                elif line.startswith(tl.TimelineEventType.LEFT_UP):
                    self.timeline.append(tl.TimelineEvent(
                        None,
                        tl.TimelineEventType.LEFT_UP,
                        TestWindow.pairtopos(pos),
                        0
                    ))
                elif line.startswith(tl.TimelineEventType.RIGHT_UP):
                    self.timeline.append(tl.TimelineEvent(
                        None,
                        tl.TimelineEventType.RIGHT_UP,
                        TestWindow.pairtopos(pos),
                        0
                    ))
        self.frame.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.frame.Show()