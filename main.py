# Define Main Function
if __name__ == '__main__':
    # Importing Python Modules:S1
    try:
        import sys
        from pathlib import Path
        import getpass
        import shutil
    except Exception as error:
        print(f'ERROR - [Main:S1] - {str(error)}')

    # Appending System Path And User-Defined Function:S2
    try:
        sys.path.append(str(Path.cwd()))
        from supportscripts.imageencode import image_encode
        from supportscripts.imageencrypt import image_encrypt
        from supportscripts.imagedecrypt import image_decrypt
        from supportscripts.imagedecode import image_decode
    except Exception as error:
        print(f'ERROR - [Main:S2] - {str(error)}')
        sys.exit(1)

    # Select Image Operation:S3
    try:
        user_choice = input('(a) -> Image Encryption\n(b) -> Image Decryption\n-> Select Option: ').strip().lower()
        if user_choice not in ('a', 'b'):
            print('-> Invalid Option. Please Select "a" Or "b".')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Main:S3] - {str(error)}')
        sys.exit(1)

    if user_choice == 'a':
        # Define Folder Paths And Validate Input:S4
        try:
            parent_folder_path = Path.cwd()
            input_images_folder_path = Path(parent_folder_path) / 'input'
            if not input_images_folder_path.is_dir():
                print('-> "input" Folder Not Present. Please Create It And Add JPG Files.')
                sys.exit(1)
            input_images_file_path_list = sorted(
                file_path for file_path in input_images_folder_path.iterdir()
                if file_path.is_file() and file_path.suffix.lower() == '.jpg'
            )
            if not input_images_file_path_list:
                raise ValueError('No JPG Files Found In "input" Folder')
            output_folder_path = Path(parent_folder_path) / 'output'
            output_folder_path.mkdir(parents = True, exist_ok = True)
            tmp_folder_path = Path(parent_folder_path) / 'tmp'
            tmp_folder_path.mkdir(parents = True, exist_ok = True)
            encoded_images_folder_path = Path(tmp_folder_path) / 'EncodeImages'
            encoded_images_folder_path.mkdir(parents = True, exist_ok = True)
            encrypted_images_folder_path = Path(tmp_folder_path) / 'EncryptedImages'
            encrypted_images_folder_path.mkdir(parents = True, exist_ok = True)
        except Exception as error:
            print(f'ERROR - [Main:S4] - {str(error)}')
            sys.exit(1)

        # Calling "image_encode" Function:S5
        try:
            image_encode_backend_response = image_encode(input_images_folder_path = str(input_images_folder_path), encoded_images_folder_path = str(encoded_images_folder_path))
            if image_encode_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S5] - {image_encode_backend_response["message"]}')
                sys.exit(1)
            else:
                print(f'-> {image_encode_backend_response["message"]}')
        except Exception as error:
            print(f'ERROR - [Main:S5] - {str(error)}')
            sys.exit(1)

        # Encrypt Encoded Text Files:S6
        try:
            encryption_password = getpass.getpass('\n-> Enter Encryption Password: ')
            image_encrypt_backend_response = image_encrypt(encoded_images_folder_path = str(encoded_images_folder_path), encrypted_images_folder_path = str(encrypted_images_folder_path), encryption_password = encryption_password)
            if image_encrypt_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S6] - {image_encrypt_backend_response["message"]}')
                sys.exit(1)
            else:
                print(f'-> {image_encrypt_backend_response["message"]}')
        except Exception as error:
            print(f'ERROR - [Main:S6] - {str(error)}')
            sys.exit(1)

        # Move Encrypted Files To "output" Folder:S7
        try:
            for encrypted_file_path in sorted(encrypted_images_folder_path.iterdir()):
                if encrypted_file_path.is_file():
                    shutil.move(str(encrypted_file_path), str(output_folder_path))
            print('\n-> Encrypted Files Moved To "output" Folder Successfully')
        except Exception as error:
            print(f'ERROR - [Main:S7] - {str(error)}')
            sys.exit(1)

        # Delete Processed Input Files And Working Folders:S8
        try:
            for input_image_file_path in input_images_file_path_list:
                input_image_file_path.unlink()
            if not any(input_images_folder_path.iterdir()):
                input_images_folder_path.rmdir()
            shutil.rmtree(encoded_images_folder_path)
            shutil.rmtree(encrypted_images_folder_path)
            if not any(tmp_folder_path.iterdir()):
                tmp_folder_path.rmdir()
        except Exception as error:
            print(f'ERROR - [Main:S8] - {str(error)}')
            sys.exit(1)

    elif user_choice == 'b':
        # Define Folder Paths And Validate Input:S9
        try:
            parent_folder_path = Path.cwd()
            input_images_folder_path = Path(parent_folder_path) / 'input'
            if not input_images_folder_path.is_dir():
                print('-> "input" Folder Not Present. Please Create It And Add Encrypted Files.')
                sys.exit(1)
            encrypted_image_file_path_list = sorted(
                file_path for file_path in input_images_folder_path.iterdir()
                if file_path.is_file()
            )
            if not encrypted_image_file_path_list:
                raise ValueError('No Encrypted Files Found In "input" Folder')
            output_folder_path = Path(parent_folder_path) / 'output'
            output_folder_path.mkdir(parents = True, exist_ok = True)
            tmp_folder_path = Path(parent_folder_path) / 'tmp'
            tmp_folder_path.mkdir(parents = True, exist_ok = True)
            encoded_images_folder_path = Path(tmp_folder_path) / 'EncodeImages'
            encoded_images_folder_path.mkdir(parents = True, exist_ok = True)
            original_images_folder_path = Path(tmp_folder_path) / 'OriginalImages'
            original_images_folder_path.mkdir(parents = True, exist_ok = True)
        except Exception as error:
            print(f'ERROR - [Main:S9] - {str(error)}')
            sys.exit(1)

        # Decrypt Encrypted Files From Input Folder:S10
        try:
            encryption_password = getpass.getpass('\n-> Enter Decryption Password: ')
            image_decrypt_backend_response = image_decrypt(input_images_folder_path = str(input_images_folder_path), encoded_images_folder_path = str(encoded_images_folder_path), encryption_password = encryption_password)
            if image_decrypt_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S10] - {image_decrypt_backend_response["message"]}')
                sys.exit(1)
            else:
                print(f'-> {image_decrypt_backend_response["message"]}')
        except Exception as error:
            print(f'ERROR - [Main:S10] - {str(error)}')
            sys.exit(1)

        # Decode Encoded Text Files To Original Images:S11
        try:
            image_decode_backend_response = image_decode(encoded_images_folder_path = str(encoded_images_folder_path), original_images_folder_path = str(original_images_folder_path))
            if image_decode_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S11] - {image_decode_backend_response["message"]}')
                sys.exit(1)
            else:
                print(f'-> {image_decode_backend_response["message"]}')
        except Exception as error:
            print(f'ERROR - [Main:S11] - {str(error)}')
            sys.exit(1)

        # Move Original Images To Output Folder:S12
        try:
            for original_image_file_path in sorted(original_images_folder_path.iterdir()):
                if original_image_file_path.is_file():
                    shutil.move(str(original_image_file_path), str(output_folder_path))
            print('\n-> Original Images Moved To "output" Folder Successfully')
        except Exception as error:
            print(f'ERROR - [Main:S12] - {str(error)}')
            sys.exit(1)

        # Delete Processed Input Files And Working Folders:S13
        try:
            for encrypted_image_file_path in encrypted_image_file_path_list:
                encrypted_image_file_path.unlink()
            if not any(input_images_folder_path.iterdir()):
                input_images_folder_path.rmdir()
            shutil.rmtree(encoded_images_folder_path)
            shutil.rmtree(original_images_folder_path)
            if not any(tmp_folder_path.iterdir()):
                tmp_folder_path.rmdir()
        except Exception as error:
            print(f'ERROR - [Main:S13] - {str(error)}')
            sys.exit(1)