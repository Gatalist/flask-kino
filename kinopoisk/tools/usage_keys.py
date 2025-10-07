import json
import os
from datetime import date


class UsageKeysToday:
    def __init__(self):
        self.usage_keys_file = '/app/tools/keys_usage.json'
        os.makedirs(os.path.dirname(self.usage_keys_file), exist_ok=True)

    def load_usage(self) -> dict:
        """Загружаем данные из файла"""
        # if not os.path.exists(self.usage_keys_file):
        #     raise FileNotFoundError
        with open(self.usage_keys_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # проверяем дату
        today = str(date.today())
        if data.get("date") != today:
            data = {"date": today, "keys": []}
            self.save_usage(data)
        return data

    def save_usage(self, data: dict) -> None:
        """Сохраняем данные в файл"""
        with open(self.usage_keys_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_key(self, api_key: str) -> None:
        """Добавляем использованный ключ (только один раз в день)"""
        data = self.load_usage()
        if api_key not in data["keys"]:
            data["keys"].append(api_key)
            self.save_usage(data)

    def is_key_used(self, api_key: str) -> bool:
        """Проверяем, использован ли ключ сегодня"""
        data = self.load_usage()
        return api_key in data["keys"]
