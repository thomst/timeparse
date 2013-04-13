from distutils.core import setup

VERSION = "0.2"

setup(
    name = "timeparse", 
    version = VERSION, 
    author = "Thomas Leichtfuss", 
    author_email = "thomaslfuss@gmx.de",
    url = "https://github.com/thomst/timeparse",
    download_url = "https://github.com/downloads/thomst/timeparse/timeparse-{version}.tar.gz".format(version=VERSION),
    description = 'timeparse is an extension for argparse to parse commandline-arguments as objects of the datetime-module.',
    long_description = "timeparse provides several classes that can be passed to the argparse.ArgumentParser.add_argument-method as action (s. documentation of argparse). With this classes an argument is parsed as date-, time-, datetime- or timedelta-object of the datetime-module.",
    py_modules = ["timeparse"],
#    package_dir = {'' : 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
    ],
    license='GPL',
    keywords='argparse datetime',
)
