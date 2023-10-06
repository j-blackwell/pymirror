from setuptools import setup, find_packages

setup(
    name="pymirror",
    version="1!0+dev",
    author_email="jrstats@outlook.com",
    packages=["app", "resources", "widgets"],
    install_requires=[
        "fastapi[all]",
        "uvicorn[standard]",
        "jinja2",
        "numpy",
        "pandas",
        "requests",
        "selenium",
        "webdriver-manager",
        "lxml",
        "html5lib",
        "beautifulsoup4"
    ],
    author="James Robinson",
    license="Apache-2.0",
    description="Python smart mirror",
)