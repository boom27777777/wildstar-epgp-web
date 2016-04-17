from epgp import app, shutdown

if __name__ == '__main__':
    app.debug = False
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print('Cleaning up...')
    shutdown()
