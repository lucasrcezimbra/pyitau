import os

from setuptools import setup


README = os.path.join(os.path.dirname(__file__), 'README.rst')
REQUIREMENTS = os.path.join(os.path.dirname(__file__), 'requirements.txt')


if __name__ == "__main__":
    setup(
        name='pyitau',
        description='Scraper to download data from Itaú Internet Banking',
        version='0.0.5',
        long_description=open(README).read(),
        author="Lucas Rangel Cezimbra",
        author_email="lucas.cezimbra@gmail.com",
        license="LGPLv2",
        url='https://github.com/Lrcezimbra/itau',
        keywords=['pyitau', 'itau', 'api', 'client', 'requests', 'banking', 'bank', 'finance', 'accounting'],
        install_requires=open(REQUIREMENTS).readlines(),
        packages=['pyitau'],
        zip_safe=False,
        include_package_data=True,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
        ],
    )
