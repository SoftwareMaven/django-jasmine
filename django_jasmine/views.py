import posixpath

from django.conf import settings
from django.views.generic import TemplateView

from django_jasmine import utils


class RunTests(TemplateView):
    """
    Run Jasmine tests.

    To use an alternate version of Jasmine, set) :attr:`jasmine_path` to the
    correct relative base. Alternatively, you can specify the exact initial
    default media by overriding :meth:`get_default_js` and
    :meth:`get_default_css`.

    By default, the configuration file looked for is ``'tests.json'``. Override
    or extend this by altering :attr:`config_names` to contain a tuple of file
    names to consider as configuration files.
    """
    template_name = 'jasmine/index.html'
    jasmine_path = 'js/lib/jasmine-1.3.0'
    coffee_path = 'js/lib/coffeescript-1.4.0'
    config_names = ('tests.json',)
    silent_config_fail = False

    def get_context_data(self, *args, **kwargs):
        """
        Add the ``jasmine_media`` and ``spec_media`` Media files to the
        context, along a list of extra templates to include called
        ``include_templates``.
        """
        css = self.get_default_css()
        js = self.get_default_js()
        coffee = self.get_default_coffeescript()

        spec_js = []
        spec_coffee = []
        templates = set()
        for config in utils.get_configs(names=self.config_names,
                                        silent=self.silent_config_fail):
            templates = templates.union(config.get('templates', ()))
            for path in config.get('js', ()):
                if path not in js:
                    js.append(path)
            for path in config.get('coffee', ()):
                if path not in coffee:
                    coffee.append(path)
            for path in config.get('spec', ()):
                spec_type = path.split('.')[-1]
                if path not in locals()[spec_type]:
                    locals()['spec_{0}'.format(spec_type)].append(path)

        data = super(RunTests, self).get_context_data(*args, **kwargs)
        data['jasmine_media'] = utils.ExtendedMedia(css=css, js=js, coffee=coffee)
        data['spec_media'] = utils.ExtendedMedia(js=spec_js, coffee=spec_coffee)
        data['include_templates'] = templates
        return data

    def get_default_coffeescript(self):
        """
        Return a Media-formatted dictionary of relative or absolute URLs to coffee-script
        files.
        """
        return [
        ]

    def get_default_css(self):
        """
        Return a Media-formatted dictionary of relative or absolute URLs to CSS
        files.
        """
        return {
            'all': [posixpath.join(self.jasmine_path, 'jasmine.css')],
        }

    def get_default_js(self):
        """
        Return a list of JavaScript files, either absolute or relative URLs.
        """
        return [
            posixpath.join(self.jasmine_path, 'jasmine.js'),
            posixpath.join(self.jasmine_path, 'jasmine-html.js'),
            posixpath.join(self.coffee_path, 'coffee-script.js'),
        ]
