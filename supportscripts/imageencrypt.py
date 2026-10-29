# Define "image_encrypt" Function
def image_encrypt(encoded_images_folder_path: str, encrypted_images_folder_path: str, encryption_password: str) -> dict[str, str]:
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

    # Creating Path Object And Check Folders Are Present:S2
    try:
        encoded_images_folder_path_object = Path(encoded_images_folder_path)
        encrypted_images_folder_path_object = Path(encrypted_images_folder_path)
        for folder in (encoded_images_folder_path_object, encrypted_images_folder_path_object):
            if not (folder.exists() and folder.is_dir()):
                return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '2', 'message': f'"{folder.name}" Folder Not Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '2', 'message': str(error)}

    # Create Encoded Text File Path List:S3
    try:
        encoded_text_file_path_list = sorted(
            file_path for file_path in encoded_images_folder_path_object.iterdir()
            if file_path.is_file() and file_path.suffix.lower() == '.txt'
        )
        if not encoded_text_file_path_list:
            raise ValueError(f'No Encoded Text Files Found In "{encoded_images_folder_path_object.name}" Folder')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '3', 'message': str(error)}

    # Empty "EncryptedImages" Folder:S4
    try:
        for output_item_path in encrypted_images_folder_path_object.iterdir():
            if output_item_path.is_dir():
                shutil.rmtree(output_item_path)
            else:
                output_item_path.unlink()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '4', 'message': str(error)}

    # Encrypt Encoded Text Files:S5
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
            encrypted_file_path = encrypted_images_folder_path_object / encoded_text_file_path.stem
            with encrypted_file_path.open('xb') as output:
                output.write(salt + ciphertext)
            print(f'{encrypted_number:03d}-> "{encoded_text_file_path.name}" Has Been Encrypted With Password')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encrypt', 'step': '5', 'message': str(error)}
    
    # Return Success:S6
    return {'status': 'SUCCESS', 'file_name': 'Image-Encrypt', 'step': '6', 'message': 'All The Images Encrypted Successfully'}