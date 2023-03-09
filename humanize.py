# A function to return human readable size from bytes

def human_read(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    base2 = 1024
    for u in units[:-1]:
        if size < base2:
            return f'{size}{u}'
        size /= base2
