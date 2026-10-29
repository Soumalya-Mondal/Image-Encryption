# Image Encryption

**A Python command-line tool for password-protected JPG encryption and recovery.**

[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Cryptography](https://img.shields.io/badge/Cryptography-50.0.2%2B-205375)](https://cryptography.io/)
[![Package Manager](https://img.shields.io/badge/Package_Manager-uv-DE5FE9)](https://docs.astral.sh/uv/)

Convert JPG images into Base64 text, encrypt them using Fernet with Argon2id-derived keys, and restore them using the same password. Files are processed locally with per-file progress messages.

> [!WARNING]
> **Back up your files before using this tool.** After all batch results have been moved to `output`, the application deletes the processed input files. Skipped files and subfolders are preserved, and `input` is removed only when empty. Use dedicated working copies, never your only copy. The generated folders inside `tmp` are application-managed and are cleared before reuse; do not store personal files there.

## Contents

- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Security and Operational Notes](#security-and-operational-notes)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)

## Features

- **Batch processing:** encrypt `.jpg` files directly inside the input folder.
- **Password-based encryption:** derive a separate key for each file using Argon2id and a random salt.
- **Authenticated encryption:** use Fernet to encrypt data and detect invalid tokens during decryption.
- **Reversible encoding:** recover the original image bytes without image recompression.
- **Interactive terminal workflow:** choose encryption or decryption and enter a password using `getpass`.
- **Readable progress:** numbered file updates, completion messages, and step-specific errors.

## Getting Started

### Requirements

| Requirement | Details |
| --- | --- |
| Python | 3.12 or newer; the repository pins 3.12 by default |
| Package manager | [uv](https://docs.astral.sh/uv/getting-started/installation/) |
| Python dependency | `cryptography>=50.0.2`, declared in [pyproject.toml](pyproject.toml) |

### Installation

1. Clone or download this repository.
2. Open a terminal in the project root.
3. Synchronize the environment using the committed dependency lockfile:

   ```powershell
   uv sync --locked
   ```

The commands below use Windows PowerShell syntax. **Always launch the application from the project root:** input, output, temporary folders, and the support-module search path are based on the current working directory.

## Usage

### Encrypt Images

1. Keep a backup of your original images outside the project working folders.
2. Create an `input` folder in the project root.
3. Copy the JPG files you want to encrypt into it:

   ```text
   input\
   |-- img001.jpg
   |-- img002.jpg
   `-- img003.jpg
   ```

4. Start the application:

   ```powershell
   uv run .\main.py
   ```

5. Select `a` and enter an encryption password.
6. Collect the extensionless encrypted files from `output`.

**Example terminal output**

```text
(a) -> Image Encryption
(b) -> Image Decryption
-> Select Option: a

001-> "img001.jpg" File Encoded Into Base64
002-> "img002.jpg" File Encoded Into Base64
-> All The Images Encoded Into Base64 Successfully

-> Enter Encryption Password:
001-> "img001.txt" Has Been Encrypted With Password
002-> "img002.txt" Has Been Encrypted With Password
-> All The Images Encrypted Successfully

-> Encrypted Files Moved To "output" Folder Successfully
```

For example, `img001.jpg` becomes an encrypted file named `img001`. Keep its name unchanged if you want to recover the same image filename.

### Decrypt Images

1. Back up your encrypted files outside the project working folders.
2. Create the `input` folder if it was removed after the previous run.
3. Place only this tool's encrypted files inside `input`. To reverse the previous run, move the encrypted files from `output` into `input`.
4. Start the application:

   ```powershell
   uv run .\main.py
   ```

5. Select `b` and enter the password used to encrypt those files.
6. Collect the restored `.jpg` images from `output`.

**Example terminal output**

```text
(a) -> Image Encryption
(b) -> Image Decryption
-> Select Option: b

-> Enter Decryption Password:
001-> "img001" Has Been Decrypted With Password
002-> "img002" Has Been Decrypted With Password
-> All The Images Decrypted Successfully

001-> "img001.txt" Has Been Decoded From Base64
002-> "img002.txt" Has Been Decoded From Base64
-> All The Images Decoded From Base64 Successfully

-> Original Images Moved To "output" Folder Successfully
```

> [!IMPORTANT]
> Move previous results to a safe location before another run to avoid output filename collisions. Decryption attempts every regular file directly inside `input`, so do not mix encrypted files with images or unrelated documents. All files in a decryption batch must use the password entered for that run.

## How It Works

### Processing Pipeline

```text
Encryption
JPG bytes -> Base64 text -> Argon2id-derived key + Fernet -> Encrypted file

Decryption
Encrypted file -> Argon2id-derived key + Fernet -> Base64 text -> JPG bytes
```

Base64 is a reversible encoding step, **not encryption**. Confidentiality and token authentication are provided by Fernet.

### Key Derivation

A fresh random salt is generated for each encrypted file. The password is UTF-8 encoded and passed to Argon2id using these parameters:

| Parameter | Value |
| --- | --- |
| Salt size | 64 bytes |
| Derived key length | 32 bytes |
| Iterations | 3 |
| Lanes | 4 |
| Memory cost | 65,536 KiB (64 MiB) |
| Fernet key encoding | URL-safe Base64 |

### Encrypted File Layout

Each encrypted file contains:

```text
+----------------------+---------------------------+
| Random salt          | Fernet token              |
| First 64 bytes       | Remaining bytes           |
+----------------------+---------------------------+
```

Decryption reads the salt, derives the key from the supplied password, and decrypts the token. The salt is stored with the encrypted data; the password is not written to the file.

There is no custom format-version header, and the Argon2id parameters are not embedded in the file. Changing those parameters or the salt size can break compatibility with existing encrypted files.

## Project Structure

```text
Image-Encryption\
|-- main.py
|-- supportscripts\
|   |-- imageencode.py
|   |-- imageencrypt.py
|   |-- imagedecrypt.py
|   `-- imagedecode.py
|-- .gitignore
|-- .python-version
|-- pyproject.toml
|-- uv.lock
`-- README.md
```

| Script | Responsibility |
| --- | --- |
| [main.py](main.py) | Menu, password prompts, workflow coordination, output moves, and cleanup |
| [imageencode.py](supportscripts/imageencode.py) | Convert JPG bytes into Base64 text files |
| [imageencrypt.py](supportscripts/imageencrypt.py) | Generate salts, derive keys, and encrypt the encoded files |
| [imagedecrypt.py](supportscripts/imagedecrypt.py) | Read salts, derive keys, and decrypt files into Base64 text |
| [imagedecode.py](supportscripts/imagedecode.py) | Decode Base64 text into JPG files |

### Working Folders

| Folder | Purpose | Lifecycle |
| --- | --- | --- |
| `input` | JPG images for encryption or encrypted files for decryption | Created by you; processed files are deleted after all results are moved, and the folder is removed only when empty |
| `output` | Encrypted files or restored JPG images | Created automatically if missing; retained |
| `tmp\EncodeImages` | Base64 text used by either workflow | Temporary |
| `tmp\EncryptedImages` | Encrypted files awaiting transfer to output | Encryption only |
| `tmp\OriginalImages` | Restored images awaiting transfer to output | Decryption only |

The working folders used by the selected operation are cleared before reuse and removed during final cleanup. Other contents of `tmp` are preserved, and the root `tmp` folder is removed only when empty. Errors can leave partial results and temporary files behind.

## Security and Operational Notes

- **Use a strong, unique password.** There is no password recovery or confirmation prompt.
- **Back up both originals and encrypted files.** Do not rely on a single encryption/decryption run as your only recovery strategy.
- **Only `.jpg` input is selected for encryption.** Matching is case-insensitive, but `.jpeg`, `.png`, and other extensions are not selected. Subfolders are not processed.
- **Image contents are not validated.** Encryption selects files by extension, and decryption writes restored files with a `.jpg` suffix.
- **Filenames remain visible.** Encrypted output keeps each input file's basename.
- **Temporary data is not encrypted at rest throughout the workflow.** Base64 text and restored images are written to disk. Normal deletion is not secure erasure.
- **Empty batches are rejected.** Encryption requires at least one `.jpg` file, and decryption requires at least one regular input file. Empty eligible-file lists return an error instead of reaching successful cleanup.
- **Conflicting JPG names are rejected.** Files that would produce the same Base64 filename, such as `photo.jpg` and `photo.JPG` on a case-sensitive filesystem, must be renamed before encryption.
- **Use one operation at a time.** Do not run multiple instances in the same project folder or modify input files while a run is active, including while entering a password. The workflow does not lock files against concurrent changes.
- **Processing and cleanup are not transactional.** A failure can leave some files processed and others unfinished. Input cleanup starts only after all batch results have been moved to `output`. Inspect leftover output before retrying; each helper clears its generated destination folder before writing new files.
- **Base64 decoding is strict.** Invalid Base64 characters and padding errors are reported rather than silently ignored. This is not a check that the decoded bytes form a valid JPEG image.
- **Files are loaded into memory.** Base64 adds size overhead, so large images require additional memory and disk space.
- **Review files before publishing to GitHub.** The [.gitignore](.gitignore) excludes `input`, `output`, and `tmp`. Ignore rules do not untrack files already committed to Git; remove any previously tracked private data from the index separately.

## Error Handling

The helper functions return dictionaries containing `status`, `file_name`, `step`, and `message`. For example, [image_decrypt](supportscripts/imagedecrypt.py) returns this response for an incorrect password or a damaged Fernet token:

```python
{
    'status': 'ERROR',
    'file_name': 'Image-Decrypt',
    'step': '4',
    'message': 'Incorrect password or damaged encrypted file: img001'
}
```

The `file_name` field identifies the helper, while `step` identifies its internal processing stage. Successful responses use `status: 'SUCCESS'` with the same fields.

The decryption helper returns error dictionaries directly, without explicitly raising `ValueError`, for:

- No encrypted input files: helper step `3`.
- An incomplete file containing no data beyond the 64-byte salt: helper step `4`.
- An incorrect password or damaged encrypted token: helper step `4`.

Other processing exceptions are caught by the relevant stage handler and returned in the same error format.

When the decryption helper returns `ERROR`, [main.py](main.py) prints the message with its CLI step identifier and exits with status `1`:

```text
ERROR - [Main:S10] - Incorrect password or damaged encrypted file: img001
```

The CLI does not proceed to image decoding, output moves, or input cleanup after that failure. Temporary files already produced earlier in the batch can remain.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `"input" Folder Not Present` | Create `input` in the project root before running either operation. |
| `No JPG Files Found In "input" Folder` | Add regular `.jpg` files directly inside `input`; other image extensions and subfolders are not processed. |
| `No Encrypted Files Found In "input" Folder` | Place this tool's encrypted files directly inside `input` before selecting decryption. |
| `JPG Files Have Conflicting Base Names` | Rename images that would produce the same encoded filename before retrying encryption. |
| `Incorrect password or damaged encrypted file` | Use the original password and an intact encrypted file produced by this tool. |
| `Invalid or incomplete encrypted file` | The file is too short to contain the expected salt and encrypted token; restore it from a backup. |
| A destination file already exists | Move previous results out of `output` before retrying. Check for partial results from the failed run. |
| Module import errors | Run from the project root and synchronize dependencies with `uv sync --locked`. |
