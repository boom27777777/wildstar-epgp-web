from epgp import app, shutdown

if __name__ == '__main__':
    app.debug = False
    try:
        app.run()
    except KeyboardInterrupt:
        print('Cleaning up...')
    shutdown()
