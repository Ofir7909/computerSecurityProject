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
        self.number_of_attempts = 5  #

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

    def is_password_valid(self, password: str) -> bool:
        if len(password) < self.password_length:
            print("length Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return False

        if self.capital_letters:
            if not any(c.isupper() for c in password):
                print("upper Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return False

        if self.small_letters:
            if not any(c.islower() for c in password):
                print("lower Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return False

        if self.special_characters:
            if not any(c in "!@#$%" for c in password):
                print("symbols Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return False

        if self.numbers:
            if not any(c in "0123456789" for c in password):
                print("number Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return False

        # can change to word in password
        if any(word == password for word in self.disallowed_words):
            print("dictionary Error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return False

        return True
