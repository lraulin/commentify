import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='commentify',
    version='0.0.2',
    entry_points={
        'console_scripts': ['commentify=commentify.commentify:main'],
    },
    author="Lee Raulin",
    author_email="leeraulin@gmail.com",
    description="Process text from clipboard.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lraulin/commentify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
