import argparse
import os
import input_window
import input_window as iw
import test_window as tw
import timeline as tl
import pyautogui
import time


def cmd_setup(args):
    app = iw.InputWindow(False)
    app.file = args.output
    app.MainLoop()


def cmd_test(args):
    if not os.path.exists("clickman.txt"):
        print('clickman.txt is not found')
        exit(1)
        return
    app = tw.TestWindow(False)
    app.file = args.input
    app.load()
    app.MainLoop()


def cmd_run(args):
    _, _, li = tl.parse(args.input)
    for event in li:
        if event.kind == tl.TimelineEventType.LEFT_DOWN:
            pyautogui.mouseDown(event.pos.x, event.pos.y, 'left')
        elif event.kind == tl.TimelineEventType.RIGHT_DOWN:
            pyautogui.mouseDown(event.pos.x, event.pos.y, 'right')
        elif event.kind == tl.TimelineEventType.LEFT_UP:
            pyautogui.mouseUp(event.pos.x, event.pos.y, 'left')
        elif event.kind == tl.TimelineEventType.RIGHT_UP:
            pyautogui.mouseUp(event.pos.x, event.pos.y, 'right')
        elif event.kind == tl.TimelineEventType.MOVE:
            pyautogui.moveTo(event.pos.x, event.pos.y)
        elif event.kind == tl.TimelineEventType.SLEEP:
            time.sleep(event.sleep)


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # `setup` コマンドの parser を作成
    parser_setup = subparsers.add_parser('setup', help='see `setup -h`')
    parser_setup.set_defaults(handler=cmd_setup)
    parser_setup.add_argument('--output', default='clickman.txt')

    # `test` コマンドの parser を作成
    parser_test = subparsers.add_parser('test', help='see `test -h`')
    parser_test.set_defaults(handler=cmd_test)
    parser_test.add_argument('--input', default='clickman.txt')

    # `run` コマンドの parser を作成
    parser_run = subparsers.add_parser('run', help='see `run -h`')
    parser_run.set_defaults(handler=cmd_run)
    parser_run.add_argument('--input', default='clickman.txt')

    # コマンドラインを解析して実行
    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
