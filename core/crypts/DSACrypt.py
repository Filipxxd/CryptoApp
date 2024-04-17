import hashlib
import base64
import os
from zipfile import ZipFile

from core.crypts.RSACrypt import RSACrypt
from core.ValidationError import ValidationError


class DSACrypt:
    def __init__(self, output_folder='./'):
        self.rsa = RSACrypt()
        self.encoding = 'utf-8'
        self.output_folder = output_folder

        self.key_separator = '_'
        self.key_prefix = 'RSA '
        self.signature_prefix = 'RSA_SHA3-512 '

        self.ext_archive = 'zip'
        self.ext_public = 'pub'
        self.ext_private = 'priv'
        self.ext_signature = 'sign'

    def sign_file(self, file_path: str, private_path: str):
        private_key = self.__decode_key(self.__get_file_content(private_path))

        bytes_content = self.__get_file_content(file_path)
        file_hash = self.__sha_hash(bytes_content)
        encrypted_hash = self.rsa.encrypt(file_hash, private_key)
        signature = self.signature_prefix + self.__string_to_base64(encrypted_hash)

        file_name = os.path.basename(file_path)
        zip_name = 'signed_' + file_name.split('.')[0]
        zip_file_path = f'{self.output_folder}/{zip_name}.{self.ext_archive}'

        with ZipFile(self.update_name_if_exists(zip_file_path), 'w') as file:
            file.writestr(f'signature.{self.ext_signature}', signature)
            file.write(file_path, os.path.basename(file_path))

    def check_signature(self, zip_path: str, public_path: str) -> bool:
        public_key = self.__decode_key(self.__get_file_content(public_path))

        with ZipFile(zip_path, 'r') as zip_file:
            files = zip_file.namelist()

            if len(files) > 2:
                raise ValidationError(f'Archive File Error - must contain only two '
                                      f'files: the signature (\'.{self.ext_signature}\')'
                                      f' and the signed file itself.')

            for file in files:
                if file.endswith(self.ext_signature):
                    signature_c = zip_file.read(file)
                else:
                    file_c = zip_file.read(file)

        without_prefix = signature_c.replace(self.signature_prefix.encode(self.encoding), b'')
        signature = self.__base64_bytes_to_string(without_prefix)

        try:
            decrypted_signature = self.rsa.decrypt(signature, public_key)
        except ValidationError:
            return False

        hashed_file = self.__sha_hash(file_c)

        return hashed_file == decrypted_signature

    def get_key_files(self):
        q = self.rsa.get_random_prime()

        while True:
            p = self.rsa.get_random_prime()
            if p != q:
                break

        public, private = self.rsa.create_keys(q, p)

        file_path = f'{self.output_folder}/private.{self.ext_private}'
        file_content = self.key_prefix + self.__string_to_base64(f'{private[0]}{self.key_separator}{private[1]}')
        self.__save_file(file_path, file_content)

        file_path = f'{self.output_folder}/public.{self.ext_public}'
        file_content = self.key_prefix + self.__string_to_base64(f'{public[0]}{self.key_separator}{public[1]}')
        self.__save_file(file_path, file_content)

    def __decode_key(self, encoded_key: bytes) -> tuple[int, int]:
        decoded_key = self.__base64_bytes_to_string(encoded_key.replace(self.key_prefix.encode(self.encoding), b''))
        key_items = [int(part) for part in (decoded_key.split(self.key_separator))]
        return key_items[0], key_items[1]

    def __string_to_base64(self, text: str) -> str:
        return base64.b64encode(text.encode(self.encoding)).decode(self.encoding)

    def __base64_bytes_to_string(self, text: bytes) -> str:
        return base64.b64decode(text).decode(self.encoding)

    def __save_file(self, file_path: str, content: str):
        with open(self.update_name_if_exists(file_path), 'w') as file:
            file.write(content)

    @staticmethod
    def __get_file_content(file_path: str) -> bytes:
        with open(file_path, 'rb') as file:
            return file.read()

    @staticmethod
    def __sha_hash(file_content: bytes) -> str:
        sha = hashlib.sha3_512()
        sha.update(file_content)
        return sha.hexdigest()

    @staticmethod
    def update_name_if_exists(path: str) -> str:
        filename, extension = os.path.splitext(path)
        counter = 1

        while os.path.exists(path):
            path = f'{filename}_{str(counter)}{extension}'
            counter += 1

        return path
