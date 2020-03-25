import argparse
import os
import input_window
import input_window as iw
import test_window as tw


def cmd_setup(args):
    app = iw.InputWindow(False)
    app.MainLoop()


def cmd_test(args):
    if not os.path.exists("clickman.txt"):
        print('clickman.txt is not found')
        exit(1)
        return
    app = tw.TestWindow(False)
    app.MainLoop()


parser: argparse.ArgumentParser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# `setup` コマンドの parser を作成
parser_setup = subparsers.add_parser('setup', help='see `setup -h`')
parser_setup.set_defaults(handler=cmd_setup)

# `test` コマンドの parser を作成
parser_test = subparsers.add_parser('test', help='see `test -h`')
parser_test.set_defaults(handler=cmd_test)

# コマンドラインを解析して実行
args = parser.parse_args()
if hasattr(args, 'handler'):
    args.handler(args)
else:
    parser.print_help()
