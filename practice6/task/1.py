filename = "sample.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write("First line\n")
    f.write("Second line\n")
    f.write("Third line\n")

print("Файл создан и данные записаны.")