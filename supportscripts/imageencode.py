# Define "image_encode" Function
def image_encode() -> dict[str, str]:
    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
        import base64
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '1', 'message': str(error)}

    # Define Folder Path:S2
    try:
        parent_folder_path = Path.cwd()
        tmp_folder_path = Path(parent_folder_path) / 'tmp'
        converted_images_folder_path = Path(tmp_folder_path) / 'ConvertedImages'
        encoded_images_folder_path = Path(tmp_folder_path) / 'EncodedImages'
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '2', 'message': str(error)}

    # Recreate "EncodedImages" Folder:S3
    try:
        if encoded_images_folder_path.exists() and encoded_images_folder_path.is_dir():
            shutil.rmtree(encoded_images_folder_path)
        encoded_images_folder_path.mkdir(parents = True, exist_ok = True)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '3', 'message': str(error)}

    # Creating Path Object And Check If "ConvertedImages" Folder Is Present:S4
    try:
        converted_images_folder_path_object = Path(converted_images_folder_path)
        if not (converted_images_folder_path_object.exists() and converted_images_folder_path_object.is_dir()):
            return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '4', 'message': f'"{converted_images_folder_path_object.name}" Folder Not Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '4', 'message': str(error)}

    # Create Input JPG File Path List:S5
    try:
        input_images_file_path_list = sorted(
            file_path for file_path in converted_images_folder_path_object.iterdir()
            if file_path.is_file() and file_path.suffix.lower() == '.jpg'
        )
        if not input_images_file_path_list:
            return {'status': 'INFO', 'file_name': 'Image-Encode', 'step': '5', 'message': f'No JPG Files Found In "{converted_images_folder_path_object.name}" Folder'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '5', 'message': str(error)}

    # Convert Input Images To Base64 Text Files:S6
    try:
        print('')
        for image_number, image_file_path in enumerate(input_images_file_path_list, start = 1):
            base64_text = base64.b64encode(image_file_path.read_bytes()).decode('ascii')
            encoded_image_file_path = encoded_images_folder_path / f'{image_file_path.stem}.txt'
            encoded_image_file_path.write_text(base64_text, encoding = 'ascii')
            print(f'{image_number:05d}-> "{image_file_path.name}" File Encoded Into Base64')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '6', 'message': str(error)}

    # Delete "ConvertedImages" Folder:S7
    try:
        shutil.rmtree(converted_images_folder_path)
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Encode', 'step': '7', 'message': str(error)}

    # Return Success:S8
    return {'status': 'SUCCESS', 'file_name': 'Image-Encode', 'step': '8', 'message': 'All The Images Encoded Into Base64 Successfully'}