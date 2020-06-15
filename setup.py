import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fast_youtube_search", # Replace with your own username
    version="0.0.1",
    author="Andres Cruz y Vera",
    author_email="andrscyv@gmail.com",
    description="Unlimited youtube search with web scrapping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrscyv/fast_youtube_search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)