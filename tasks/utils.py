import os

def is_newer(file1, file2):
    """
    Is `file1` newer than `file2`?

    Args:
        file1 (str): Path to a file
        file2 (str): Path to a file
    """
    mt1 = os.path.getmtime(file1)
    mt2 = os.path.getmtime(file2)

    return mt1 > mt2
