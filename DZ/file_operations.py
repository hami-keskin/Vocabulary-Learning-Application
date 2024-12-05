import json

def load_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Ensure that the file is not empty
            content = file.read().strip()
            if content:
                return json.loads(content)
            else:
                return {}  # Return an empty dictionary if the file is empty
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}  # Return an empty dictionary if the JSON is invalid

def save_words(file_path, words):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(words, file, ensure_ascii=False, indent=4)
