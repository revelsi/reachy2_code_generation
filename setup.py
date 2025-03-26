from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="reachy-code-generation",
    version="0.1.0",
    author="",
    author_email="",
    description="A code generation interface for the Reachy 2 robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/reachy_function_calling",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "reachy-gradio=launch_code_gen:main",
        ],
    },
) 