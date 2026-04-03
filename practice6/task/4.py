import shutil

source_file = "sample.txt"
copy_file = "sample_copy.txt"
backup_file = "sample_backup.txt"

shutil.copy(source_file, copy_file)
print("Файл скопирован в sample_copy.txt")

shutil.copy(source_file, backup_file)
print("Резервная копия создана: sample_backup.txt") 