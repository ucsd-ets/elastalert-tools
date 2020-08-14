import setuptools

setuptools.setup(
    name="elastalert_tools", # Replace with your own username
    version="0.0.1",
    author="Wesley Uykimpang",
    author_email="wuykimpang@ucsd.edu",
    description="Code handlers for elastalert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests', 
        'elastalert',
        'kubernetes',
        'oo-tools'
    ],
    python_requires='>=3.6',
    setup_requires = ['pytest-runner', 'elastalert'],
    tests_require = ['pytest'],
    package_data={'elastalert_tools': ['*.py']}
)