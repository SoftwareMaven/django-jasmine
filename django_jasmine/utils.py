import json
import logging
import posixpath

from django.contrib.staticfiles.finders import get_finders

logger = logging.getLogger("django_jasmine")


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
