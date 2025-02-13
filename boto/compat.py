# Copyright (c) 2012 Amazon.com, Inc. or its affiliates.  All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
import os

# This allows boto modules to say "from boto.compat import json".  This is
# preferred so that all modules don't have to repeat this idiom.
try:
    import simplejson as json
except ImportError:
    import json


# Switch to use encodebytes, which deprecates encodestring in Python 3
try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes


# If running in Google App Engine there is no "user" and
# os.path.expanduser() will fail. Attempt to detect this case and use a
# no-op expanduser function in this case.
try:
    os.path.expanduser('~')
    expanduser = os.path.expanduser
except (AttributeError, ImportError):
    # This is probably running on App Engine.
    expanduser = (lambda x: x)

from boto.vendored import six

from boto.vendored.six import BytesIO, StringIO
from boto.vendored.six.moves import filter, http_client, map, _thread, \
                                    urllib, zip
from boto.vendored.six.moves.queue import Queue
from boto.vendored.six.moves.urllib.parse import parse_qs, quote, unquote, \
                                                 urlparse, urlsplit
from boto.vendored.six.moves.urllib.parse import unquote_plus
from boto.vendored.six.moves.urllib.request import urlopen

if six.PY3:
    # StandardError was removed, so use the base exception type instead
    StandardError = Exception
    long_type = int
    from configparser import ConfigParser
    unquote_str = unquote_plus
else:
    StandardError = StandardError
    long_type = long
    from ConfigParser import SafeConfigParser as ConfigParser

    def unquote_str(value, encoding='utf-8'):
        # In python2, unquote() gives us a string back that has the urldecoded
        # bits, but not the unicode parts.  We need to decode this manually.
        # unquote has special logic in which if it receives a unicode object it
        # will decode it to latin1.  This is hard coded.  To avoid this, we'll
        # encode the string with the passed in encoding before trying to
        # unquote it.
        byte_string = value.encode(encoding)
        return unquote_plus(byte_string).decode(encoding)

# Create a wrapper function to get a non-validating SSL context (boto
# implements its own certificate validation) on Python versions that
# have that concept.
try:
    from ssl import create_default_context as _create_default_context
    def create_non_validating_ssl_context(cafile=None):
        ctx = _create_default_context(cafile=cafile)
        ctx.check_hostname = False
        return ctx
except ImportError:
    def create_non_validating_ssl_context(cafile=None):
        return None
