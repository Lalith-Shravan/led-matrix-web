import os

def getFileExtension(file_path):
    """
    Get the file extension of a file based on its name or path.

    :param file_path: The file name or path.
    :return: The file extension (e.g., 'txt', 'jpg') or an empty string if no extension exists.
    """
    return os.path.splitext(file_path)[1][1:]  # Remove the leading dot (.)

if __name__ == "__main__":
    # Example usage:
    file_path = "example/image.png"
    extension = getFileExtension(file_path)
    print(extension)  # Output: 'png'