import os
from cryptography.fernet import Fernet


class LevelsIO:

    _KEY_FILE = 'Utilities/encryption_key.key'
    _DATA_FILE = 'Utilities/completed_levels.enc'

    @staticmethod
    def get_completed_levels():
        return LevelsIO._get_completed_levels(LevelsIO._read_completed_levels_data())

    @staticmethod
    def _get_cipher():
        if not os.path.exists(LevelsIO._KEY_FILE):
            key = Fernet.generate_key()
            with open(LevelsIO._KEY_FILE, 'wb') as key_file:
                key_file.write(key)
        else:
            with open(LevelsIO._KEY_FILE, 'rb') as key_file:
                key = key_file.read()

        return Fernet(key)

    @staticmethod
    def complete_level(game_id, level_number):
        file_data = LevelsIO._read_completed_levels_data()
        if LevelsIO._is_level_completed(game_id, level_number, file_data):
            return

        while len(file_data) <= game_id:
            file_data.append('')
        file_data[game_id] += ' ' + str(level_number)

        cipher = LevelsIO._get_cipher()
        encrypted_data = cipher.encrypt('\n'.join(file_data).encode())
        with open(LevelsIO._DATA_FILE, 'wb') as file:
            file.write(encrypted_data)

    @staticmethod
    def _read_completed_levels_data():
        if not os.path.exists(LevelsIO._DATA_FILE):
            return []

        cipher = LevelsIO._get_cipher()
        with open(LevelsIO._DATA_FILE, 'rb') as file:
            encrypted_data = file.read()
            decrypted_data = cipher.decrypt(encrypted_data).decode()
            file_data = [row.strip() for row in decrypted_data.split('\n')]
        return file_data

    @staticmethod
    def _is_level_completed(game_id, level_number, file_data):
        if len(file_data) < game_id + 1:
            return False
        for level in file_data[game_id].split():
            if int(level) == level_number:
                return True
        return False

    @staticmethod
    def _get_completed_levels(file_data):
        levels = []
        for row in file_data:
            completed = set()
            for element in row.split():
                completed.add(int(element))
            levels.append(completed)
        while len(levels) < 4:
            levels.append(set())
        return levels