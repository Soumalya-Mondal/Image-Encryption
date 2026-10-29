# Define "image_encode" Function
def image_encode(input_images_folder_path: str, encoded_images_folder_path: str) -> dict[str, str]:
    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
        import base64
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '1', 'message': str(error)}

    # Creating Path Object And Check Folders Are Present:S2
    try:
        input_images_folder_path_object = Path(input_images_folder_path)
        encode_images_folder_path_object = Path(encoded_images_folder_path)
        for folder in (input_images_folder_path_object, encode_images_folder_path_object):
            if not (folder.exists() and folder.is_dir()):
                return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '2', 'message': f'"{folder.name}" Folder Not Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '2', 'message': str(error)}

    # Create Input JPG File Path List:S3
    try:
        input_images_file_path_list = sorted(
            file_path for file_path in input_images_folder_path_object.iterdir()
            if file_path.is_file() and file_path.suffix.lower() == '.jpg'
        )
        if not input_images_file_path_list:
            raise ValueError(f'No JPG Files Found In "{input_images_folder_path_object.name}" Folder')
        encoded_image_file_path_set = {
            encode_images_folder_path_object / f'{file_path.stem}.txt'
            for file_path in input_images_file_path_list
        }
        if len(encoded_image_file_path_set) != len(input_images_file_path_list):
            raise ValueError('JPG Files Have Conflicting Base Names; Rename Them Before Encryption')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '3', 'message': str(error)}

    # Empty "EncodeImages" Folder:S4
    try:
        for output_item_path in encode_images_folder_path_object.iterdir():
            if output_item_path.is_dir():
                shutil.rmtree(output_item_path)
            else:
                output_item_path.unlink()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '4', 'message': str(error)}
    
    # Convert Input Images To Base64 Text Files:S5
    try:
        print('')
        for image_number, image_file_path in enumerate(input_images_file_path_list, start = 1):
            base64_text = base64.b64encode(image_file_path.read_bytes()).decode('ascii')
            encoded_image_file_path = encode_images_folder_path_object / f'{image_file_path.stem}.txt'
            encoded_image_file_path.write_text(base64_text, encoding = 'ascii')
            print(f'{image_number:03d}-> "{image_file_path.name}" File Encoded Into Base64')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '5', 'message': str(error)}

    # Return Success:S6
    return {'status': 'SUCCESS', 'file_name': 'Image-Encode', 'step': '6', 'message': 'All The Images Encoded Into Base64 Successfully'}