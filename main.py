# Define Main Function
if __name__ == '__main__':
    # Importing Python Modules:S1
    try:
        import sys
        from pathlib import Path
        import getpass
    except Exception as error:
        print(f'ERROR - [Main:S1] - {str(error)}')

    # Appending System Path And User-Defined Function:S2
    try:
        sys.path.append(str(Path.cwd()))
        from supportscripts.imageconvert import image_convert
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

    # Enter Password And Confirm Password:S4
    try:
        encryption_password = getpass.getpass('\n-> Enter Password: ')
        confirm_password = getpass.getpass('-> Confirm Password: ')
        if encryption_password != confirm_password:
            print('-> Password And Confirm Password Do Not Match.')
            sys.exit(1)
    except Exception as error:
        print(f'ERROR - [Main:S4] - {str(error)}')
        sys.exit(1)

    if user_choice == 'a':
        print('')
        # Define Folder Paths And Validate Input:S5
        try:
            parent_folder_path = Path.cwd()
            images_folder_path = Path(parent_folder_path) / 'images'
        except Exception as error:
            print(f'ERROR - [Main:S5] - {str(error)}')
            sys.exit(1)

        # Calling "image_convert" Function:S6
        try:
            image_convert_backend_response = image_convert(images_folder_path = str(images_folder_path))
            if image_convert_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S6] - {image_convert_backend_response["message"]}')
                sys.exit(1)
            else:
                print(f'-> {image_convert_backend_response["message"]}')
        except Exception as error:
            print(f'ERROR - [Main:S6] - {str(error)}')
            sys.exit(1)

        # Calling "image_encode" Function:S7
        try:
            image_encode_backend_response = image_encode()
            if image_encode_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S7] - {image_encode_backend_response["message"]}')
                sys.exit(1)
            elif image_encode_backend_response['status'] == 'INFO':
                print(f'-> {image_encode_backend_response["message"]}')
                sys.exit(0)
            else:
                print(f'-> {image_encode_backend_response["message"]}')
                print('')
        except Exception as error:
            print(f'ERROR - [Main:S7] - {str(error)}')
            sys.exit(1)

        # Encrypt Encoded Text Files:S8
        try:
            image_encrypt_backend_response = image_encrypt(images_folder_path = str(images_folder_path), encryption_password = encryption_password)
            if image_encrypt_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S8] - {image_encrypt_backend_response["message"]}')
                sys.exit(1)
            else:
                print(f'-> {image_encrypt_backend_response["message"]}')
        except Exception as error:
            print(f'ERROR - [Main:S8] - {str(error)}')
            sys.exit(1)

    elif user_choice == 'b':
        print('')
        # Define Folder Paths And Validate Input:S11
        try:
            parent_folder_path = Path.cwd()
            images_folder_path = Path(parent_folder_path) / 'images'
        except Exception as error:
            print(f'ERROR - [Main:S11] - {str(error)}')
            sys.exit(1)

        # Decrypt Encrypted Files From "images" Folder:S12
        try:
            image_decrypt_backend_response = image_decrypt(images_folder_path = str(images_folder_path), encryption_password = encryption_password)
            if image_decrypt_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S12] - {image_decrypt_backend_response["message"]}')
                sys.exit(1)
            else:
                print(f'-> {image_decrypt_backend_response["message"]}')
        except Exception as error:
            print(f'ERROR - [Main:S12] - {str(error)}')
            sys.exit(1)

        # Decode Encoded Text Files To Original Images And Copy To "images" Folder:S13
        try:
            image_decode_backend_response = image_decode(images_folder_path = str(images_folder_path))
            if image_decode_backend_response['status'] == 'ERROR':
                print(f'ERROR - [Main:S13] - {image_decode_backend_response["message"]}')
                sys.exit(1)
            else:
                print(f'-> {image_decode_backend_response["message"]}')
        except Exception as error:
            print(f'ERROR - [Main:S13] - {str(error)}')
            sys.exit(1)
