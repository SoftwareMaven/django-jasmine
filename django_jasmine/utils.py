import json
import logging
import posixpath
from itertools import chain
try:
    from urllib.parse import urljoin
except ImportError:     # Python 2
    from urlparse import urljoin

import django.forms
from django.conf import settings
from django.forms import Media
from django.forms import widgets
from django.utils.html import format_html
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.staticfiles.finders import get_finders
from django.utils.safestring import mark_safe

logger = logging.getLogger("django_jasmine")

widgets.MEDIA_TYPES += (u'coffee',)

@python_2_unicode_compatible
class ExtendedMedia(object):
    '''
    Support media types beyond js and css.
    '''
    def __init__(self, media=None, **kwargs):
        # Should have one of these for each type added to MEDIA_TYPES
        if media:
            media_attrs = media.__dict__
        else:
            media_attrs = kwargs

        self._css = {}
        self._js = []
        self._coffee = []

        for name in widgets.MEDIA_TYPES:
            getattr(self, 'add_' + name)(media_attrs.get(name, None))
        # del_list = []
        # for type, value in kwargs.iteritems():
        #     if type in (widgets.MEDIA_TYPES):
        #         continue
        #     setattr(self, '_{0}'.format(type), value)
        #     del_list.append(type)
        # for item in del_list:
        #     del kwargs[item]
        # super(ExtendedMedia, self).__init__(media=media, **kwargs)

    def __str__(self):
        return self.render()

    def render(self):
        return mark_safe('\n'.join(chain(*[getattr(self, 'render_' + name)() for name in widgets.MEDIA_TYPES])))

    def render_js(self):
        return [format_html('<script type="text/javascript" src="{0}"></script>', self.absolute_path(path)) for path in self._js]

    def render_css(self):
        # To keep rendering order consistent, we can't just iterate over items().
        # We need to sort the keys, and iterate over the sorted list.
        media = sorted(self._css.keys())
        return chain(*[
                [format_html('<link href="{0}" type="text/css" media="{1}" rel="stylesheet" />', self.absolute_path(path), medium)
                    for path in self._css[medium]]
                for medium in media])

    def render_coffee(self):
        return [format_html('<script type="text/coffeescript" src="{0}"></script>', self.absolute_path(path)) for path in self._coffee]

    def absolute_path(self, path, prefix=None):
        if path.startswith(('http://', 'https://', '/')):
            return path
        if prefix is None:
            if settings.STATIC_URL is None:
                 # backwards compatibility
                prefix = settings.MEDIA_URL
            else:
                prefix = settings.STATIC_URL
        return urljoin(prefix, path)

    def __getitem__(self, name):
        "Returns a Media object that only contains media of the given type"
        if name in widgets.MEDIA_TYPES:
            return self.__class__(**{str(name): getattr(self, '_' + name)})
        raise KeyError('Unknown media type "%s"' % name)


    def add_js(self, data):
        if data:
            for path in data:
                if path not in self._js:
                    self._js.append(path)

    def add_css(self, data):
        if data:
            for medium, paths in data.items():
                for path in paths:
                    if not self._css.get(medium) or path not in self._css[medium]:
                        self._css.setdefault(medium, []).append(path)

    def add_coffee(self, data):
        if data:
            for path in data:
                if path not in self._coffee:
                    self._coffee.append(path)

    def __add__(self, other):
        combined = self.__class__()
        for name in widgets.MEDIA_TYPES:
            getattr(combined, 'add_' + name)(getattr(self, '_' + name, None))
            getattr(combined, 'add_' + name)(getattr(other, '_' + name, None))
        return combined


widgets.Media = ExtendedMedia
django.forms.Media = ExtendedMedia

def get_configs(names=('tests.json',), silent=False):
    """
    Find all configuration files throughout the project, parsing each and
    returning them as a list of dictionaries.
    """
    configs = {}
    for finder in get_finders():
        for path, storage in finder.list(ignore_patterns=None):
            if posixpath.basename(path) not in names:
                continue
            if path in configs:
                continue

            contents = storage.open(path).read()
            try:
                data = json.loads(contents)
                if not isinstance(data, dict):
                    raise ValueError("Expected a configuration dictionary")
                configs[path] = data
            except ValueError:
                if not silent:
                    raise ValueError("Invalid JSON config file: %s" % path)
                logging.error("Skipping invalid JSON config file: %s" % path)

    sorted_configs = sorted([
        (not data.get('priority'), posixpath.dirname(path), data)
        for path, data in configs.iteritems()
    ])
    return [parts[-1] for parts in sorted_configs]
