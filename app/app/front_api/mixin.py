from flask import jsonify
from app.settings import Config
import math



class Mixin:
    def responce_object(self, obj: object, model_schema: object) -> object:
        schema = model_schema(many=False)
        results = schema.dump(obj)
        return jsonify(results)

    def responce_many_objects(self, obj: object, model_schema: object) -> object:
        # Используйте схему Marshmallow для маршалинга данных
        schema = model_schema(many=True)
        return schema.dump(obj)
    
    def objects_in_page(self, page: int, obj: object) -> object:
        # Вычислите начальный и конечный индексы для выборки фильмов
        start = (page - 1) * Config.PAGINATE_ITEM_IN_PAGE
        end = start + Config.PAGINATE_ITEM_IN_PAGE
        # Выберите обьекты для текущей страницы
        return obj[start:end]

    def json_result(self, page: int, marshmallig: object, obj: object):
        pagination = {}
        if page:
            pagination["pages"] = math.ceil(obj.count() / Config.PAGINATE_ITEM_IN_PAGE)
            pagination["curent_page"] = page
            pagination["item_in_page"] = Config.PAGINATE_ITEM_IN_PAGE
        pagination["items"] = obj.count()

        results = {
            "pagination": pagination,
            "objects": marshmallig
        }

        return jsonify(results)