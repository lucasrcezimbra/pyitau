import os

from setuptools import setup

README = os.path.join(os.path.dirname(__file__), 'README.rst')


if __name__ == "__main__":
    setup(
        name='pyitau',
        description='Scraper to download data from Itaú Internet Banking',
        version='1.0.3',
        long_description=open(README).read(),
        author="Lucas Rangel Cezimbra",
        author_email="lucas.cezimbra@gmail.com",
        license="LGPLv2",
        url='https://github.com/lucasrcezimbra/pyitau',
        keywords=['pyitau', 'itau', 'api', 'client', 'requests',
                  'banking', 'bank', 'finance', 'accounting'],
        install_requires=['beautifulsoup4', 'requests'],
        packages=['pyitau'],
        zip_safe=False,
        include_package_data=True,
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',
        ],
    )
