from cx_Freeze import setup, Executable
from modules.utils import absolute_path

build_exe_options = {
    "build_exe": absolute_path("build\\dist"),
    "include_files": [
        absolute_path("config.ini"),
        absolute_path("LICENSE"),
        absolute_path("README.md"),
    ],
    "zip_exclude_packages": ["ahk"],
    "zip_include_packages": "*",
    "optimize": 2,
}

setup(
    name="MH-HP-Overlay",
    version="1.0.0",
    author="Alexander-Lancellott",
    description="A simple HP overlay application",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            absolute_path("overlay.py"),
            target_name="MH-HP-Overlay",
            base="console",
            icon=absolute_path("overlay.ico"),
        )
    ],
)
