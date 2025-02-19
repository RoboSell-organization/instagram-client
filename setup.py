from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="instagram-client",
    version="0.1.6",
    packages=find_packages(),
    author="Abdulvoris",
    author_email="erkinovabdulvoris101@gmail.com",
    description="Instagram official api 2.0 client by robosell.uz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RoboSell-organization/instagram-client",
    install_requires=[
        "requests>=2.0.0",
        "python-dateutil>=2.8.0",
        "pydantic>=1.9.0",
        "typing_extensions>=4.0.0"
    ],
    python_requires=">=3.8",
)
