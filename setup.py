from distutils.core import setup

from os import path
from setuptools import find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='trtokenizer',
    # packages=['trtopicter'],
    packages=find_packages(),
    include_package_data=True,
    version='0.0.3',
    license='MIT',
    description='Sentence and word tokenizers for the Turkish language',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Apdullah YAYIK',
    author_email='apdullahyayik@gmail.com',
    url='https://github.com/apdullahyayik/TrTokenizer',
    download_url='https://github.com/apdullahyayik/TrTokenizer/archive/refs/tags/0.0.3.tar.gz',
    keywords=['sentence tokenizer', 'word tokenizer', 'Turkish language', 'natural language processing'],
    install_requires=['regex'],
    python_requires='>=3.4'
)
