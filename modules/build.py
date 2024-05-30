import subprocess
import os


def absolute_path(path: str = ''):
    return os.path.abspath(path).replace('\\modules', '')


def main():
    path = absolute_path('setup_cx.py')
    py_path = absolute_path('.venv\\Scripts\\python')

    command_options = [
        py_path, path, 'build'
    ]

    subprocess.run(command_options)


if __name__ == "__main__":
    main()
