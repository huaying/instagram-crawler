from setuptools import setup


setup(name='inscrawler',
      version='1.2.0.dev1',
      description='Instagram Crawler',
      url='https://github.com/huaying/ins-crawler',
      author='Huaying Tsai',
      author_email='royal3501@gmail.com',
      license='MIT',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
      keywords=['instagram crawler'],
      install_requires=['selenium'],
      packages=['inscrawler'],
      zip_safe=False)
