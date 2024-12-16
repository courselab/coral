#  SPDX-FileCopyrightText: 2023 Monaco F. J. <monaco@usp.br>
#  SPDX-FileCopyrightText: 2024 Coral authors <git@github.com/courselab/coral>
#   
#  SPDX-License-Identifier: GPL-3.0-or-later
#
#  This file is part of Cobra, a derivative work of KobraPy.

import json

class Translator:
    _instance = None  # Singleton instance
    available_languages = ["english", "portuguese"]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Translator, cls).__new__(cls)
        return cls._instance

    def __init__(self, file_path="assets/translation.json", default_language="english"):
        if not hasattr(self, "initialized"):
            self.translations = {}
            self.default_language = default_language
            if file_path:
                self.load_translations(file_path)
            self.initialized = True  # Ensures __init__ runs only once

    def load_translations(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.translations = json.load(file)
        except FileNotFoundError:
            raise Exception(f"Translation file '{file_path}' not found.")
        except json.JSONDecodeError:
            raise Exception("Translation file is not a valid JSON.")

    def set_language(self, language):
        if language not in self.translations:
            raise ValueError(f"Language '{language}' not available in translations.")
        self.default_language = language

    def message(self, code):
        if self.default_language not in self.translations:
            raise ValueError(f"Default language '{self.default_language}' not loaded.")
        return self.translations[self.default_language].get(
            code, f"[{code}] message not found."
        )

# Example usage
if __name__ == "__main__":
    # First initialization
    translator = Translator("translation.json")
    print(translator.message("welcome_message"))  # Output: Welcome to our application!

    # Second initialization (same instance will be reused)
    another_translator = Translator()
    another_translator.set_language("portuguese")
    print(another_translator.message("welcome_message"))  # Output: Bem-vindo ao nosso aplicativo!

    # Confirming that both variables refer to the same instance
    print(translator is another_translator)  # Output: True

