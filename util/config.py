import os
from collections import namedtuple
from tempfile import mkdtemp
from .helpers import yaml_from_file, print_if_debug
# fix this if config2 works
from .environ_key import key, environ_key

class Config:

    def __init__(self, **kwargs):
        self._yaml = None
        self._url = None
        self._tmp_dir = None

        for _key in key:
            # prefer kwarg over environ.
            # see if key is in kwargs
            attr = kwargs.get(_key)
            if attr is None:
                # try to get attr from the environ
                try:
                    env_key = getattr(environ_key, _key)
                    attr = os.environ.get(env_key)
                except AttributeError:
                    pass
            # set the attr (or None) on self for key
            if _key is key.url:
                self._url = attr
            elif _key is key.tmp_dir:
                self._tmp_dir = attr
            else:
                if attr is None:
                    attr = ''

                setattr(self, _key, attr)

        self._set_defaults()
        
    def _set_defaults(self):
        defaults = {
                key.host: 'localhost',
                key.port: '3141',
                key.scheme: 'http',
                key.certs: '/certs',
                key.config_path: '/config/devpi.yml',
        }
        # set any default values that did not get set above.
        for _key in defaults:
            attr = getattr(self, _key, None)
            if attr is None or attr == '':
                setattr(self, _key, defaults[_key])

        return True

    def url(self):
        if self._url is None:
            return '{0}://{1}:{2}/'.format(self.scheme, self.host, self.port)
        return self._url

    def tmp_dir(self):
        if self._tmp_dir is None:
            self._tmp_dir = mkdtemp(prefix='devpi_')
            os.environ[environ_key.tmp_dir] = self._tmp_dir
        return self._tmp_dir

    def yaml(self):
        if self._yaml is None:
            if self.config_path is None:
                print_if_debug(prefix='Config', message='{} not set'.format(key.config_path))
                return None
            self._yaml = yaml_from_file(self.config_path)
        return self._yaml

    def load_directive(self, directive):
        if self.yaml:
            _directive = self.yaml().get(directive)
            if _directive is None:
                print_if_debug(prefix='Config', message="Could not find config directive for '{}'"\
                    .format(directive))

            for k, v in _directive.items():
                setattr(self, k, v)

    def export(self):
        for _key in key:
            env_key = getattr(environ_key, _key)
            value = getattr(self, _key, '')
            if _key == 'url' or _key == 'tmp_dir' and value != '':
                os.environ[env_key] = str(value())
            else:
                os.environ[env_key] = str(value)

        return True
