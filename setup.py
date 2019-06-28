import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="banhammer.py",
    version="1.0.0",
    license="GPLv3+",
    author="Mariavi developers",
    author_email="moravrav@gmail.com",
    description="A Discord integration framework for Reddit moderation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dan6erbond/Banhammer-Framework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
