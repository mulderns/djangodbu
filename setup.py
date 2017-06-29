from distutils.core import setup
setup(
  name = 'djangodbu',
  packages = ['djangodbu'], # this must be the same as the name above
  version = '0.0.1rc1',
  description = 'Tools for debugging django',
  author = 'Valtteri Kortesmaa',
  author_email = 'mulderns@iki.fi',
  license='MIT',
  url = 'https://github.com/mulderns/djangodbu',
  download_url = 'https://github.com/mulderns/archive/0.0.1.tar.gz',
  keywords = ['django', 'debug', 'shell_plus', 'orm'], # arbitrary keywords
  classifiers=[
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',

      # Indicate who your project is intended for
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Debug Tools',

      # Pick your license as you wish (should match "license" above)
      'License :: OSI Approved :: MIT License',

      # Specify the Python versions you support here. In particular, ensure
      # that you indicate whether you support Python 2, Python 3 or both.
      #'Programming Language :: Python :: 2',
      #'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      #'Programming Language :: Python :: 3',
      #'Programming Language :: Python :: 3.2',
      #'Programming Language :: Python :: 3.3',
      #'Programming Language :: Python :: 3.4',
  ],
)
