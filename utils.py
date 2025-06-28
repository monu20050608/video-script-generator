def save_text_file(content, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
