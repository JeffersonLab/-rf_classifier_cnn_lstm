import os
from rfwtools.config import Config


# Get rfwtools to read the config in the test directory
file = os.path.join(os.path.dirname(__file__), 'rfwtools.cfg')
Config()
Config().read_config_file(file)
