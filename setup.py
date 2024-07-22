from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="face-tracking-web-app",
    version="0.1.0",
    author="Darky",
    description="A web-based face tracking application using Flask and OpenCV",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xD4rky/tracker/tree/main",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=[
        "Flask>=2.0.0",
        "opencv-python>=4.5.0",
        "cvzone>=1.5.0",
        "numpy>=1.19.0",
    ],
    entry_points={
        "console_scripts": [
            "face-tracker=app:main",
        ],
    },
)