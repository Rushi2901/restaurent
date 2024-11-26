# Python script to convert file encoding to UTF-8
with open('db.json', 'rb') as f:
    content = f.read()

# Decode with detected encoding and encode to UTF-8
content = content.decode('utf-16')  # Or another encoding you found
with open('db_utf8.json', 'w', encoding='utf-8') as f:
    f.write(content)
