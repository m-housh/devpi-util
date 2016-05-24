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
        'tmp_path'])

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
        tmp_path='DEVPI_TMP_PATH'
)
