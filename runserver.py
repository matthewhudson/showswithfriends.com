from app import flask_app


flask_app.run(debug=flask_app.config['DEBUG'],
              host='0.0.0.0',
              port=flask_app.config['PORT'])
