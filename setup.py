from setuptools import setup, find_packages

setup(
    name="MH-HP-Overlay-For-3DS-Emulator",
    author="Alexander-Lancellott",
    author_email="alejandrov.lancellotti@gmail.com",
    version="1.1.5",
    packages=find_packages(),
    install_requires=[
        "ahk[binary]==1.8.0",
        "ahk-wmutil==0.1.0",
        "colorama==0.4.6",
        "PySide6==6.7.2",
        "cursor==1.3.5",
        "psutil==6.1.0",
        "pywin32==306",
        "cx_Freeze",
        "art==6.2",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["build = modules.build:main"],
    },
)
