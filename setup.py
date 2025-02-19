from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="instagram-client",
    version="0.1.3",
    packages=find_packages(),
    author="Abdulvoris",
    author_email="erkinovabdulvoris101@gmail.com",
    description="Instagram official api 2.0 client by robosell.uz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RoboSell-organization/instagram-client",
    install_requires=[
        "annotated-types>=0.7.0",
        "anyio>=4.8.0",
        "certifi>=2025.1.31",
        "charset-normalizer>=3.4.1",
        "idna>=3.10",
        "pydantic>=2.10.6",
        "python-dateutil>=2.9.0",
        "python-dotenv>=1.0.1",
        "requests>=2.32.0",
        "sniffio>=1.3.1",
        "starlette>=0.45.3",
        "typing_extensions>=4.12.2",
        "urllib3>=2.3.0"
    ],
    python_requires=">=3.8",
)
