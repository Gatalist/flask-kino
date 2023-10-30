from flask_restful import Api
from app import app
from .swagger_doc import Apispec_docs
from .routes import MoviesMany, GenreMany, CountryMany, DirectorMany, ReliaseMany
from .routes import MoviesOne, GenreOne, CountryOne, DirectorOne, ReliaseOne


front_api = Api(app)
front_docs_api = Apispec_docs(app)



front_api.add_resource(MoviesMany, '/movies/<page>')
front_docs_api.register(MoviesMany)

front_api.add_resource(MoviesOne, '/movies/<movie_id>')
front_docs_api.register(MoviesOne)


front_api.add_resource(GenreMany, '/genre')
front_docs_api.register(GenreMany)

front_api.add_resource(GenreOne, '/genre/<genre_id>')
front_docs_api.register(GenreOne)


front_api.add_resource(CountryMany, '/country')
front_docs_api.register(CountryMany)

front_api.add_resource(CountryOne, '/country/<country_id>')
front_docs_api.register(CountryOne)


front_api.add_resource(DirectorMany, '/director')
front_docs_api.register(DirectorMany)

front_api.add_resource(DirectorOne, '/director/<director_id>')
front_docs_api.register(DirectorOne)


front_api.add_resource(ReliaseMany, '/reliase')
front_docs_api.register(ReliaseMany)

front_api.add_resource(ReliaseOne, '/reliase/<reliase_id>')
front_docs_api.register(ReliaseOne)

