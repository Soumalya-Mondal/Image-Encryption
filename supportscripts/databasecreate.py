# Define "database_create" Function
def database_create(database_folder_path: str) -> dict[str, str]:
    # Importing Python Modules:S1
    try:
        from pathlib import Path
        import sqlite3
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Database-Create', 'step': '1', 'message': str(error)}

    # Define Folder Path:S2
    try:
        database_folder_path_object = Path(database_folder_path)
        image_encryption_database_file_path = Path(database_folder_path_object) / 'ImageEncryption.db'
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Database-Create', 'step': '2', 'message': str(error)}

    # Check If Database Already Exists:S3
    try:
        if ((image_encryption_database_file_path.exists()) and (image_encryption_database_file_path.is_file())):
            return {'status': 'INFO', 'file_name': 'Database-Create', 'step': '3', 'message': 'Database Already Exists'}
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Database-Create', 'step': '3', 'message': str(error)}

    # Create "raw_images_details" Table:S4
    try:
        raw_images_details_table_creation_query = '''
            CREATE TABLE IF NOT EXISTS raw_images_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                file_id TEXT NOT NULL CHECK(LENGTH(file_id) = 6),
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL DEFAULT 'jpg' CHECK(file_type IN ('heic', 'jpg', 'jpeg', 'png')),
                file_size_bytes BIGINT NOT NULL,
                file_hash TEXT NOT NULL
            )
        '''
        with sqlite3.connect(str(image_encryption_database_file_path)) as db_connection:
            db_cursor = db_connection.cursor()
            db_cursor.execute(raw_images_details_table_creation_query)
            db_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Database-Create', 'step': '4', 'message': str(error)}

    # Create "converted_images_details" Table:S5
    try:
        converted_images_details_table_creation_query = '''
            CREATE TABLE IF NOT EXISTS converted_images_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                raw_file_id TEXT NOT NULL CHECK(LENGTH(raw_file_id) = 6),
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL DEFAULT 'jpg' CHECK(file_type = 'jpg'),
                file_size_bytes BIGINT NOT NULL,
                file_hash TEXT NOT NULL
            )
        '''
        with sqlite3.connect(str(image_encryption_database_file_path)) as db_connection:
            db_cursor = db_connection.cursor()
            db_cursor.execute(converted_images_details_table_creation_query)
            db_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Database-Create', 'step': '5', 'message': str(error)}

    # Create "encrypted_images_details" Table:S6
    try:
        encrypted_images_details_table_creation_query = '''
            CREATE TABLE IF NOT EXISTS encrypted_images_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                raw_file_id TEXT NOT NULL CHECK(LENGTH(raw_file_id) = 6),
                file_name TEXT NOT NULL,
                file_size_bytes BIGINT NOT NULL,
                file_hash TEXT NOT NULL
            )
        '''
        with sqlite3.connect(str(image_encryption_database_file_path)) as db_connection:
            db_cursor = db_connection.cursor()
            db_cursor.execute(encrypted_images_details_table_creation_query)
            db_connection.commit()
    except Exception as error:
        return {'status': 'ERROR', 'file_name': 'Database-Create', 'step': '6', 'message': str(error)}

    # Return Success:S7
    return {'status': 'SUCCESS', 'file_name': 'Database-Create', 'step': '7', 'message': 'Database Created Successfully'}