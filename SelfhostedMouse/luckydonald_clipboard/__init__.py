import platform

__all__ = ['Clipboard']

if platform.system() == 'Windows':  # os.name == 'nt'
    pass  # todo throw
elif platform.system() == 'Linux':
    pass  # todo throw
elif platform.system() == 'Darwin':  # Mac OS X
    from .clipboard_mac import Clipboard
else:
    pass  # todo throw
# end if