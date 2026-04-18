from setuptools import setup, find_packages

setup(
    name="path-to",
    version="1.0.0",
    description="A command-line tool to find the full path to files",
    author="Your Name",
    author_email="your.email@example.com",
    py_modules=["path_to_final"],
    entry_points={
        "console_scripts": [
            "path-to=path_to_final:main",
        ],
    },
    python_requires=">=3.6",
    install_requires=[
        "pyinstaller>=4.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
