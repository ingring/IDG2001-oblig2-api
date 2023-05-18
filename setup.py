from setuptools import setup, find_packages

if __name__ == '__main__':
    # setup()

    setup(
        name='idg2001_oblig2_api',
        version='1.0.0',
        description='IDG2001 oblig2 main api',
        packages=find_packages('src'),
        package_dir={'': 'src'},
    )
