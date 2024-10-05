from setuptools import setup, find_packages

setup(
    name='podcast-chatbot',
    version='0.1.0',
    description='A chatbot system that provides conversational experiences based on podcast transcripts.',
    author='Usama Puward',
    author_email='usamafuward2001@gmail.com',
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'Flask==2.1.3',
        'transformers==4.27.4',
        'torch==2.0.1',
        'nltk==3.8.1',
        'scikit-learn==1.2.2',
        'numpy==1.23.5',
        'pandas==1.5.3',
        'beautifulsoup4==4.11.2',
        'requests==2.28.2',
        'youtube-transcript-api==0.4.4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
