import argparse
import sys


class TerseHelpFormatter(argparse.HelpFormatter):
    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            super()._format_action_invocation(action)

        default = self._get_default_metavar_for_optional(action)
        args_string = self._format_args(action, default)

        return '{} {}'.format(', '.join(action.option_strings), args_string)

output_formats = ('text', 'wiki', 'json')


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=TerseHelpFormatter)

    parser.add_argument('files', metavar='FILE', nargs='+', help='ROMs, discs, etc.')

    parser.add_argument('-x', '--extract', action='store_true', help='extract files from disc data tracks')
    parser.add_argument('-f', '--format', action='store', default='text', choices=output_formats, metavar='FORMAT',
                        help='use output format: text (default), wiki, json', dest='output_format')

    parser.add_argument('--skip-sector-errors', action='store_true', help='skip sector error checks')  # TODO temporary

    current_module = sys.modules[__name__]
    parser.parse_args(namespace=current_module)
