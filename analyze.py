import json
import config
from handlers import handlers


def pretty_print(obj, indent=0):
    padding = ' ' * indent * 2

    if isinstance(obj, dict):
        if obj.get('type', '') == 'file_list':
            # File list.
            files = obj['value']

            longest_path = max(len(file['path']) for file in files.values())
            path_padding = min(40, longest_path + 1)

            pretty = ''
            for file in files.values():
                pretty += '{}{:<{}}({}, crc32: {}, sector: {}, {} bytes)\n'.format(padding, file['path'], path_padding,
                                                                                   file['date'], file['crc32'],
                                                                                   file['sector'], file['size'])

            return pretty

        else:
            pretty = ''
            for key, value in obj.items():
                pretty_value = pretty_print(value, indent + 1)
                if '\n' in pretty_value:
                    pretty += '{}{}:\n{}\n'.format(padding, key, pretty_value)
                else:
                    pretty += '{}{}: {}\n'.format(padding, key, pretty_value.lstrip())

            return pretty
    else:
        return '{}{}'.format(padding, obj)


def find_handler(file, file_name):
    for handler_class in handlers:
        handler = handler_class(file=file, file_name=file_name)
        if handler.test():
            return handler

    return None


def analyze_file(file, file_name):
    handler = find_handler(file, file_name)
    if not handler:
        return

    handler.get_info()

    # TODO
    if config.output_format == 'text':
        print(pretty_print(handler.info))
    elif config.output_format == 'json':
        print(json.dumps(handler.info, default=lambda obj: str(obj)))
