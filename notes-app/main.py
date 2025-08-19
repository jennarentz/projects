from website import create_app

app = create_app()

#only if the file __main__ is ran the web server will run (doesn't work for imports)
if __name__ == '__main__':
    #runs the application and updates when code is changed
    app.run(debug=True)

