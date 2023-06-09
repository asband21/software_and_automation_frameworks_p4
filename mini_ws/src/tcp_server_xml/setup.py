from setuptools import setup

package_name = 'tcp_server_xml'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='klyx',
    maintainer_email='qw41ha@student.aau.dk',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'server_node = tcp_server_xml.server_node:main',
            'subcriber = tcp_server_xml.subcriber:main'
        ],
    },
)
