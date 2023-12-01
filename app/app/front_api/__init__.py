from flask_restful import Api
from app import app
from .swagger_doc import Apispec_docs
from .routes import MoviesMany, GenreMany, CountryMany, DirectorMany, ReliaseMany, MoviesSearch
from .routes import MoviesOne, GenreOne, CountryOne, DirectorOne, ReliaseOne


front_api = Api(app)
front_api_docs = Apispec_docs(app)



front_api.add_resource(MoviesMany, '/movie/page/<page>')
front_api_docs.register(MoviesMany)

front_api.add_resource(MoviesOne, '/movie/<movie_id>')
front_api_docs.register(MoviesOne)


front_api.add_resource(MoviesSearch, '/movie/search/<name>/<page>')
front_api_docs.register(MoviesSearch)


front_api.add_resource(GenreMany, '/genre')
front_api_docs.register(GenreMany)

front_api.add_resource(GenreOne, '/genre/<genre_id>/<page>')
front_api_docs.register(GenreOne)


front_api.add_resource(CountryMany, '/country')
front_api_docs.register(CountryMany)

front_api.add_resource(CountryOne, '/country/<country_id>/<page>')
front_api_docs.register(CountryOne)


front_api.add_resource(DirectorMany, '/director/<page>')
front_api_docs.register(DirectorMany)

front_api.add_resource(DirectorOne, '/director/<director_id>/<page>')
front_api_docs.register(DirectorOne)


front_api.add_resource(ReliaseMany, '/reliase')
front_api_docs.register(ReliaseMany)

front_api.add_resource(ReliaseOne, '/reliase/<reliase_id>/<page>')
front_api_docs.register(ReliaseOne)

