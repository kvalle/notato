from os.path import dirname, normpath

USERNAME = 'kjetil'
PASSWORD = '24bd2b3885a9282c8f292344754955677b65ec6d'
SECRET_KEY = 'dev_key'
DEBUG = True
DATABASE = 'notato'
NOTATO_HOME = normpath(dirname(__file__)+'/../')
FILES_DIR = NOTATO_HOME + "/files/"