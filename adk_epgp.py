from epgp import app, shutdown
from sys import argv

if __name__ == '__main__':
    port = 6000
    if '--debug' in argv:
        app.debug = True
        port = 5000
    if '--ci' in argv:
        exit(0)
    try:
        app.run(port=port)
    except KeyboardInterrupt:
        print('Cleaning up...')
    shutdown()
