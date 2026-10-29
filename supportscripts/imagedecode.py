# Define "image_decode" Function
def image_decode(encoded_images_folder_path: str, original_images_folder_path: str) -> dict[str, str]:
    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import shutil
        import base64
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Decode', 'step': '1', 'message': str(error)}

    # Creating Path Object And Check Folders Are Present:S2
    try:
        encoded_images_folder_path_object = Path(encoded_images_folder_path)
        original_images_folder_path_object = Path(original_images_folder_path)
        for folder in (encoded_images_folder_path_object, original_images_folder_path_object):
            if not (folder.exists() and folder.is_dir()):
                return {'status': 'ERROR', 'file_name': 'Image-Decode', 'step': '2', 'message': f'"{folder.name}" Folder Not Present'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Decode', 'step': '2', 'message': str(error)}

    # Create Encoded Text File Path List And Empty "OriginalImages" Folder:S3
    try:
        encoded_text_file_path_list = sorted(
            file_path for file_path in encoded_images_folder_path_object.iterdir()
            if file_path.is_file() and file_path.suffix.lower() == '.txt'
        )
        if not encoded_text_file_path_list:
            raise ValueError(f'No Encoded Text Files Found In "{encoded_images_folder_path_object.name}" Folder')
        for output_item_path in original_images_folder_path_object.iterdir():
            if output_item_path.is_dir():
                shutil.rmtree(output_item_path)
            else:
                output_item_path.unlink()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Decode', 'step': '3', 'message': str(error)}

    # Convert Base64 Text Files To Original Images:S4
    try:
        print('')
        for decoded_number, encoded_text_file_path in enumerate(encoded_text_file_path_list, start = 1):
            image_bytes = base64.b64decode(encoded_text_file_path.read_bytes(), validate = True)
            original_image_file_path = original_images_folder_path_object / f'{encoded_text_file_path.stem}.jpg'
            original_image_file_path.write_bytes(image_bytes)
            print(f'{decoded_number:03d}-> "{encoded_text_file_path.name}" Has Been Decoded From Base64')
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Image-Decode', 'step': '4', 'message': str(error)}

    # Return Success:S5
    return {'status': 'SUCCESS', 'file_name': 'Image-Decode', 'step': '5', 'message': 'All The Images Decoded From Base64 Successfully'}
