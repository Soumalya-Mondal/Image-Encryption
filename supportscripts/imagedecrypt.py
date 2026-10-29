# Define "image_decrypt" Function
def image_decrypt(input_images_folder_path: str, encoded_images_folder_path: str, encryption_password: str) -> dict[str, str]:
    # Define Constant
    SALT_SIZE = 64

    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
        import base64
        from cryptography.fernet import Fernet, InvalidToken
        from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Decrypt', 'step': '1', 'message': str(error)}

    # Creating Path Object And Check Folders Are Present:S2
    try:
        input_images_folder_path_object = Path(input_images_folder_path)
        encoded_images_folder_path_object = Path(encoded_images_folder_path)
        if not (input_images_folder_path_object.exists() and input_images_folder_path_object.is_dir()):
            return {'status': 'ERROR', 'file_name': 'Image-Decrypt', 'step': '2', 'message': f'"{input_images_folder_path_object.name}" Folder Not Present'}
        encoded_images_folder_path_object.mkdir(parents = True, exist_ok = True)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Decrypt', 'step': '2', 'message': str(error)}

    # Create Encrypted File Path List And Empty "EncodeImages" Folder:S3
    try:
        encrypted_image_file_path_list = sorted(
            file_path for file_path in input_images_folder_path_object.iterdir()
            if file_path.is_file()
        )
        if not encrypted_image_file_path_list:
            return {'status': 'ERROR', 'file_name': 'Image-Decrypt', 'step': '3', 'message': f'No Encrypted Files Found In "{input_images_folder_path_object.name}" Folder'}
        for output_item_path in encoded_images_folder_path_object.iterdir():
            if output_item_path.is_dir():
                shutil.rmtree(output_item_path)
            else:
                output_item_path.unlink()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Decrypt', 'step': '3', 'message': str(error)}

    # Decrypt Encrypted Files:S4
    try:
        for decrypted_number, encrypted_image_file_path in enumerate(encrypted_image_file_path_list, start = 1):
            encrypted_data = encrypted_image_file_path.read_bytes()
            if len(encrypted_data) <= SALT_SIZE:
                return {'status': 'ERROR', 'file_name': 'Image-Decrypt', 'step': '4', 'message': f'Invalid or incomplete encrypted file: {encrypted_image_file_path.name}'}
            salt = encrypted_data[:SALT_SIZE]
            ciphertext = encrypted_data[SALT_SIZE:]
            kdf = Argon2id(
                salt = salt,
                length = 32,
                iterations = 3,
                lanes = 4,
                memory_cost = 64 * 1024,
            )
            decryption_key = base64.urlsafe_b64encode(kdf.derive(encryption_password.encode('utf-8')))
            try:
                plaintext = Fernet(decryption_key).decrypt(ciphertext)
            except InvalidToken:
                return {'status': 'ERROR', 'file_name': 'Image-Decrypt', 'step': '4', 'message': f'Incorrect password or damaged encrypted file: {encrypted_image_file_path.name}'}
            decrypted_file_path = encoded_images_folder_path_object / f'{encrypted_image_file_path.name}.txt'
            decrypted_file_path.write_bytes(plaintext)
            print(f'{decrypted_number:03d}-> "{encrypted_image_file_path.name}" Has Been Decrypted With Password')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Decrypt', 'step': '4', 'message': str(error)}

    # Return Success:S5
    return {'status': 'SUCCESS', 'file_name': 'Image-Decrypt', 'step': '5', 'message': 'All The Images Decrypted Successfully'}
