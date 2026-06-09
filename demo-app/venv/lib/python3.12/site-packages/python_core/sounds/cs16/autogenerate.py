
import os
from string import Template

if __name__ == '__main__':
    implicit_folder = "original"

    function_template = """
    def {filename}_sound():
        play_commands(sounds_json, "{filename}")
    """

    dest_file = "cs16.py"
    with open(dest_file, "a+", encoding="utf-8") as f:
        
        for file in os.listdir(implicit_folder):
            filename = file.split(".")[0]
            if "-" in filename:
                filename = filename.replace("-", "_")
            f.write(function_template.format(filename=filename))