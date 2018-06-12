# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)


from AppKit import NSPasteboard
from Foundation import NSImage, NSArray, NSString, NSUTF8StringEncoding


class Clipboard(object):
    FORMAT_CONVERTER = {
        'text/html': 'public.html',
        'html': 'public.html',

        'text/rtf': 'public.rtf',
        'rtf': 'public.rtf',

        'text': 'public.utf8-plain-text',
        'text/plain': 'public.utf8-plain-text',

        'image/png': 'public',
        'png': 'public.png',
    }
    def _f(self, fmt):
        return self.FORMAT_CONVERTER[fmt]
    # end def

    def copy_img(self, image_data, mime='image/png', clear_first=True):
        image = NSImage.alloc().initWithData_(image_data)
        array = NSArray.arrayWithObject_(image)
        pb = NSPasteboard.generalPasteboard()
        if clear_first:
            pb.clearContents()
        # end def
        if mime in self.FORMAT_CONVERTER:
            pb.declareTypes_owner_([self._f(mime)], None)
        # end def
        success = pb.writeObjects_(array)
        return success  # todo: throw
    # end def

    def copy_text(self, text, clear_first=True):
        if not text:
            raise ValueError('no input')
        # end if
        if isinstance(text, str):
            text = {'text/plain': text}
        # end if
        if not isinstance(text, dict):
            raise ValueError('wrong')
        # end if

        pb = NSPasteboard.generalPasteboard()
        if clear_first:
            pb.clearContents()
        # end def
        pb.declareTypes_owner_([self._f(fmt) for fmt in text.keys()], None)

        for fmt, value in text.items():
            new_str = NSString.stringWithString_(value).nsstring()
            new_data = new_str.dataUsingEncoding_(NSUTF8StringEncoding)
            pb.setData_forType_(new_data, self._f(fmt))
        # end def
    # end def
# end class
