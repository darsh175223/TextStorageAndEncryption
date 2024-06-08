# Text Storer Application

## Overview

The Text Storer Application is a Python-based GUI program for storing and retrieving text data using a JSON database. It supports both normal and line-by-line storage modes, with encryption for the stored text. The GUI is implemented using Tkinter, and encryption is handled by the `cryptography` library.

## Features

- **Normal Mode**: 
  - Enter a subject and body text.
  - The subject is stored as plain text.
  - The body text is encrypted before being stored.
  - Clear the input fields after committing the text.

- **Line-by-Line Mode**:
  - Enter a subject and a single line of text.
  - The subject is stored as plain text.
  - Each line of text is encrypted before being stored.
  - Clear the text line field after committing the line.

- **Normal Retrieval Mode**:
  - View all subjects stored in normal mode.
  - Select a subject to view the corresponding decrypted body text.

- **Line-by-Line Retrieval Mode**:
  - View all subjects stored in line-by-line mode.
  - Navigate through subjects and view the decrypted lines of text.

## Requirements

- Python 3.x
- `tkinter` library (usually included with Python)
- `cryptography` library

## Installation

1. Clone the repository or download the source code.

```bash
git clone https://github.com/yourusername/text-storer.git
cd text-storer
```

2. Install the required Python package.
```bash
pip install cryptography
```
## Usage
Run the main script to start the application:
```bash
python main.py
```
## Normal Mode
1. Select "Normal Mode".
2. Enter a subject and body text.
3. Click "Commit" to store the text. The subject is stored as plain text, and the body text is encrypted.

## Line-by-Line Mode
1. Select "Line-by-Line Mode".
2. Enter a subject and a single line of text.
3. Click "Commit Line" to store the line. The subject is stored as plain text, and the line is encrypted.
4. Repeat to add more lines to the same subject.

## File Structure
- main.py: The main script containing the GUI and application logic.
- text_storage.json: The JSON database file where text data is stored.




