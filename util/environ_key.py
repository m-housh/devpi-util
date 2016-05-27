from collections import namedtuple

EnvironKey = namedtuple('EnvrionKey', 
        ['host', 
        'port', 
        'scheme', 
        'user', 
        'index',
        'config_path', 
        'certs', 
        'url', 
        'password', 
        'requests_bundle', 
        'pip_target',
        'tmp_dir',
        'debug']
)

key = EnvironKey(
        host='host',
        port='port',
        scheme='scheme',
        user='user',
        index='index',
        config_path='config_path',
        certs='certs',
        url='url',
        password='password',
        requests_bundle='requests_bundle',
        pip_target='pip_target',
        tmp_dir='tmp_dir',
        debug='debug'
)
        

environ_key = EnvironKey(
        host='DEVPI_HOST',
        port='DEVPI_PORT',
        scheme='DEVPI_SCHEME',
        user='DEVPI_USER',
        index='DEVPI_INDEX',
        config_path='DEVPI_CONFIG_PATH',
        certs='DEVPI_CERTS',
        url='DEVPI_URL',
        password='DEVPI_PASSWORD',
        requests_bundle='REQUESTS_CA_BUNDLE',
        pip_target='PIP_TARGET',
        tmp_dir='DEVPI_TMP_DIR',
        debug='DEBUG'
)
