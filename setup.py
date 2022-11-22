from setuptools import setup

APP= ['searchAndShowResult.py']
OPTIONS = {
    'arg_emulation': True,
}
setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)