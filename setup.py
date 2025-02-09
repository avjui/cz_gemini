from setuptools import setup, find_packages
import pathlib

base = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (base / "README.md").read_text(encoding="utf-8")

setup(
    name="cz_gemini",
    version="0.3.0",

    packages = ['cz_gemini/templates'],
    package_data={'cz_gemini/templates':['*'],},

    package_dir={
        'cz_gemini': 'cz_gemini',
    },

    py_modules=[
                "cz_gemini/cz_gemini",
                "cz_gemini/gemini_ai",
                "cz_gemini/gemini_defaults",
                "cz_gemini/gemini_exception"
                ],
    #license="MIT",
    description="plugin for autocommit or spellcheck and auto correction",
    long_description=long_description,
    install_requires=[
        "commitizen", 
        "google-generativeai"
        ],
    entry_points={"commitizen.plugin": ["cz_gemini = cz_gemini.cz_gemini:GeminiCz"]},

)