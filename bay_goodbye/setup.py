from setuptools import find_packages, setup

package_name = 'bay_goodbye'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hasin023',
    maintainer_email='hasinmahtab.alvee@gmail.com',
    description='A package to say goodbye to the world',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'bay_node = bay_goodbye.bay_node:main'
        ],
    },
)
