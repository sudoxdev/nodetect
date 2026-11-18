from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="nodetect",
    version="1.0.1",
    description="High-performance stealth browser automation & persistent profile engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mitul Islam",
    author_email="mitulislam483@gmail.com",
    url="https://github.com/sudoxdev/nodetect",
    packages=find_packages(),
    install_requires=[
        "playwright>=1.40.0",
        "curl_cffi>=0.7.0",
        "click>=8.1.0",
        "rich>=13.0.0"
    ],
    entry_points={
        "console_scripts": [
            "nodetect=nodetect.cli:main"
        ]
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Testing"
    ]
)

