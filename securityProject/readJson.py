import json


class PassConfig:
    def __init__(self):
        self.password_length = 6
        self.capital_letters = False
        self.small_letters = False
        self.special_characters = False
        self.numbers = False
        self.history_of_passwords = 1  #
        self.disallowed_words = []
        self.number_of_attempts = 2  #

    def read_config(self, file_path):
        with open(file_path, "r") as json_file:
            config_data: dict = json.load(json_file)
        self.password_length = config_data.get("password_length", self.password_length)
        self.capital_letters = config_data.get("capital_letters", self.capital_letters)
        self.small_letters = config_data.get("small_letters", self.small_letters)
        self.special_characters = config_data.get(
            "special_characters", self.special_characters
        )
        self.numbers = config_data.get("numbers", self.numbers)
        self.history_of_passwords = config_data.get(
            "history_of_passwords", self.history_of_passwords
        )
        self.disallowed_words = config_data.get(
            "disallowed_words", self.disallowed_words
        )
        self.number_of_attempts = config_data.get(
            "number_of_attempts", self.number_of_attempts
        )
        return self

    def is_password_valid(self, password: str) -> str:
        if len(password) < self.password_length:
            return f"Password must be at least {self.password_length} characters long"

        if self.capital_letters:
            if not any(c.isupper() for c in password):
                return "Password must include a capital letter"

        if self.small_letters:
            if not any(c.islower() for c in password):
                return "Password must include a lowercase letter"

        if self.special_characters:
            if not any(c in "!@#$%" for c in password):
                return "Password must include a symbol"

        if self.numbers:
            if not any(c in "0123456789" for c in password):
                return "Password must include a number"

        # can change to word in password
        if any(word == password for word in self.disallowed_words):
            return "Password is too common"

        return ""
