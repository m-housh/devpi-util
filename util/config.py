import os
from collections import namedtuple
from .helpers import yaml_from_file, print_if_debug
from .environ_key import environ_key as key

class Config:
    
    def __init__(self, *args, **kwargs):
        self._yaml = None

    @property
    def host(self):
        return os.environ.get(key.host, 'localhost')

    @host.setter
    def host(self, value):
        os.environ[key.host] = str(value)
        return self.host

    @property
    def port(self):
        return os.environ.get(key.port, 3141)

    @port.setter
    def port(self, value):
        os.environ[key.port] = str(value)
        return self.port


    @property
    def scheme(self):
        return os.environ.get(key.scheme, 'http')

    @scheme.setter
    def scheme(self, value):
        os.environ[key.scheme] = str(value)
        return self.scheme
    
    @property
    def user(self):
        return os.environ.get(key.user)

    @user.setter
    def user(self, value):
        os.environ[key.user] = str(value)
        return self.user

    @property
    def index(self):
        return os.environ.get(key.index)

    @index.setter
    def index(self, value):
        os.environ[key.index] = str(value)

    @property
    def config_path(self):
        return os.environ.get(key.config_path, '/config/devpi.yml')

    @config_path.setter
    def config_path(self, value):
        os.environ[key.config_path] = str(value)
        return self.config_path

    @property
    def certs(self):
        return os.environ.get(key.certs, '/certs')

    @certs.setter
    def certs(self, value):
        os.environ[key.certs] = str(value)
        return self.certs
    
    @property
    def url(self):
        _url = os.environ.get(key.url)
        if _url is None:
            return '{0}://{1}:{2}'.format(self.scheme, self.host, self.port)
        return _url

    @url.setter
    def url(self, value):
        os.environ[key.url] = str(value)
        return self.url

    @property
    def password(self):
        return os.environ.get(key.password)

    @password.setter
    def password(self, value):
        os.environ[key.password] = str(value)
        return self.password

    @property
    def yaml(self):
        if self._yaml is None:
            if self.config_path is None:
                print_if_debug(prefix='Config', message='{} not set'.format(key.config_path))
                return None
            self._yaml = yaml_from_file(self.config_path)
        return self._yaml

    def load_directive(self, directive):
        if self.yaml:
            _directive = self.yaml.get(directive)
            if _directive is None:
                print_if_debug(prefix='Config', message="Could not find config directive for '{}'"\
                    .format(directive))

            for k, v in _directive.items():
                setattr(self, k, v)
