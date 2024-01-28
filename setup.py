from distutils.core import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'Topsis_Chhavi_102103605',         
  packages = ['Topsis_Chhavi_102103605'],  
  version = '0.2',     
  license='MIT',    
  description = 'This library will help you apply TOPSIS to your datasets for multiple criteria decision making',
  long_description=long_description,
  long_description_content_type='text/markdown', 
  author = 'Chhavi Dhankhar',                   
  author_email = 'chhavidhankhar07@gmail.com',      
  url = 'https://github.com/Chdh11/Topsis-Chhavi-102103605',   
  download_url = 'https://github.com/Chdh11/Topsis-Chhavi-102103605/archive/refs/tags/v_01.tar.gz',  
  keywords = ['TOPSIS', 'DECISION-MAKING', 'RANK'],  
  install_requires=[           
          'pandas'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)