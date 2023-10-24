from flask_apispec.extension import FlaskApiSpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin



class Apispec_docs():
    def __init__(self, app):
        self.docs = FlaskApiSpec()
        self.docs.init_app(app)
        # swagger settings
        app.config.update({
            'APISPES_SPEC': APISpec(
                title='Video',
                version='v1',
                openapi_version='2.0',
                plugins=[MarshmallowPlugin()],
            ),
            'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
            'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
        })

    def register(self, function):
        self.docs.register(function)

