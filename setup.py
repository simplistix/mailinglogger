import os

from setuptools import setup, find_packages

this_dir = os.path.dirname(__file__)

setup(
    name='mailinglogger',
    version=open(os.path.join(this_dir,'mailinglogger','version.txt')).read().strip(),
    author='Chris Withers',
    author_email='chris@simplistix.co.uk',
    license='MIT',
    description="Enhanced emailing handlers for the python logging package.",
    long_description=open(os.path.join(this_dir,'docs','description.txt')).read(),
    url='https://github.com/Simplistix/mailinglogger',
    keywords="logging email",
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications :: Email',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['six'],
    extras_require=dict(
        test=['coverage', 'coveralls', 'pytest', 'sybil', 'testfixtures'],
        build=['sphinx', 'pkginfo', 'setuptools-git', 'wheel', 'twine',
               'sphinx_rtd_theme'],
        )
    )
