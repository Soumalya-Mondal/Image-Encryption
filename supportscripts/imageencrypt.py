# Define "image_encrypt" Function
def image_encrypt(output_images_folder_path: str, encryption_password: str) -> dict[str, str]:
    # Define Constant
    SALT_SIZE = 64

    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
        import base64
        import secrets
        from cryptography.fernet import Fernet
        from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '1', 'message': str(error)}

    # Define Folder Path:S2
    try:
        parent_folder_path = Path.cwd()
        tmp_folder_path = Path(parent_folder_path) / 'tmp'
        encoded_images_folder_path = Path(tmp_folder_path) / 'EncodedImages'
        encrypted_images_folder_path = Path(tmp_folder_path) / 'EncryptedImages'
        output_images_folder_path_object = Path(output_images_folder_path)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '2', 'message': str(error)}

    # Recreate "EncryptedImages" Folder:S3
    try:
        if encrypted_images_folder_path.exists() and encrypted_images_folder_path.is_dir():
            shutil.rmtree(encrypted_images_folder_path)
        encrypted_images_folder_path.mkdir(parents = True, exist_ok = True)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '3', 'message': str(error)}

    # Empty "output" Folder:S4
    try:
        if output_images_folder_path_object.exists() and output_images_folder_path_object.is_dir():
            for output_item_path in output_images_folder_path_object.iterdir():
                if output_item_path.is_dir():
                    shutil.rmtree(output_item_path)
                else:
                    output_item_path.unlink()
        else:
            output_images_folder_path_object.mkdir(parents = True, exist_ok = True)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '4', 'message': str(error)}

    # Create Encoded Text File Path List:S5
    try:
        encoded_text_file_path_list = sorted(
            file_path for file_path in encoded_images_folder_path.iterdir()
            if file_path.is_file() and file_path.suffix.lower() == '.txt'
        )
        if not encoded_text_file_path_list:
            raise ValueError(f'No Encoded Text Files Found In "{encoded_images_folder_path.name}" Folder')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '5', 'message': str(error)}

    # Encrypt Encoded Text Files:S6
    try:
        for encrypted_number, encoded_text_file_path in enumerate(encoded_text_file_path_list, start = 1):
            plaintext = encoded_text_file_path.read_bytes()
            salt = secrets.token_bytes(SALT_SIZE)
            kdf = Argon2id(
                salt = salt,
                length = 32,
                iterations = 3,
                lanes = 4,
                memory_cost = 64 * 1024,
            )
            encryption_key = base64.urlsafe_b64encode(kdf.derive(encryption_password.encode('utf-8')))
            ciphertext = Fernet(encryption_key).encrypt(plaintext)
            encrypted_file_path = encrypted_images_folder_path / encoded_text_file_path.stem
            with encrypted_file_path.open('xb') as output:
                output.write(salt + ciphertext)
            print(f'{encrypted_number:05d}-> "{encoded_text_file_path.name}" Has Been Encrypted With Password')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '6', 'message': str(error)}

    # Copy Encrypted Files To "output" Folder And Delete "tmp" Folder:S7
    try:
        for encrypted_file_path in sorted(encrypted_images_folder_path.iterdir()):
            if encrypted_file_path.is_file():
                shutil.copy(str(encrypted_file_path), str(output_images_folder_path_object))
        shutil.rmtree(tmp_folder_path)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '7', 'message': str(error)}

    # Return Success:S8
    return {'status': 'SUCCESS', 'file_name': 'Image-Encrypt', 'step': '8', 'message': 'All The Images Encrypted Successfully'}
