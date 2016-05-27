import os
from tempfile import mkdtemp
from .helpers import yaml_from_file, print_if_debug
# fix this if config2 works
from .environ_key import key, environ_key

class Config:
    """ The main class for the application.  It stores config variables for a devpi-client
    session.

    Config options can be passed in via command line options or read in from a yaml type
    file.

    **Kwargs:**
        .. note::
            The kwargs for this are passed in from the command line options, and should
            not need to be directly accessed.

    """

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
        """ Set's default values for the necessities if not set from environment or 
        as command line options.
        """
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
        """ Set's up the url for the session, if not set via command line or environment
        variables.

        **Returns:**
            * **String** of the url for this session.
        """
        if self._url is None:
            return '{0}://{1}:{2}/'.format(self.scheme, self.host, self.port)
        return self._url

    def tmp_dir(self):
        """ Creates a temporary directory, or returns one if exists, for this devpi-client
        session.

        **Returns:**
            * **Path** to the tmp directory.
        """
        if self._tmp_dir is None:
            self._tmp_dir = mkdtemp(prefix='devpi_')
            os.environ[environ_key.tmp_dir] = self._tmp_dir
        return self._tmp_dir

    def yaml(self):
        """ A proxy for loading the config from a yaml file.  And reads any *global* settings.
        If already read this session, then returns what's already in memory.

        **Returns**:
            * **None** if the config_path variable is not set for this config instance
            * **Dict** of the yaml file at config_path.
        """
        if self._yaml is None:
            if self.config_path is None:
                print_if_debug(prefix='Config', message='{} not set'.format(key.config_path))
                return None
            self._yaml = yaml_from_file(self.config_path)
            self.load_direct('global')
        return self._yaml

    def load_directive(self, directive):
        """ Loads a directive from the config file, and set's any relevent attributes on this
        config instance, for the devpi-client session.

        **Args:**
            * **directive** (*str*):
                A string mapped to a key in the yaml config file.  Loads the child keys for
                this config instance.

        **Returns:**
            * **None**
        """
        if self.yaml:
            _directive = self.yaml().get(directive)
            if _directive is None:
                print_if_debug(prefix='Config', message="Could not find config directive for '{}'"\
                    .format(directive))

            for k, v in _directive.items():
                setattr(self, k, v)

    def export(self):
        """ Exports all the necessary environment variables, for the devpi-client session 
        commands.


        **Returns:**
            * **True**
        """
        for _key in key:
            env_key = getattr(environ_key, _key)
            value = getattr(self, _key, '')
            if _key == 'url' or _key == 'tmp_dir' and value != '':
                os.environ[env_key] = str(value())
            else:
                os.environ[env_key] = str(value)

        return True
