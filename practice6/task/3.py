filename = "sample.txt"

with open(filename, "a", encoding="utf-8") as f:
    f.write("Fourth line\n")
    f.write("Fifth line\n")

print("Новые строки добавлены.\n")

with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

print("Обновлённое содержимое файла:")
print(content)