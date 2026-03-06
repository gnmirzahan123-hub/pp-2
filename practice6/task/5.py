import os

filename = "sample_copy.txt"

if os.path.exists(filename):
    os.remove(filename)
    print(f"Файл {filename} удалён.")
else:
    print(f"Файл {filename} не найден.")