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
        "numpy<2",
        "pandas",
        "requests",
        "selenium",
        "webdriver-manager",
        "lxml",
        "html5lib",
        "beautifulsoup4",
        "glom",
        "apscheduler",
        "duckdb",
    ],
    author="James Robinson",
    license="Apache-2.0",
    description="Python smart mirror",
)
