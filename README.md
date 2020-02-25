# CatchEmAll
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

The aim of this project is to test random credentials found in data dumps. 
Precisely every credential, which is saved on a db, is used to test access in all the websites listed in [Pokedex section](#pokedex). 
  
## Warning
This software can't be used for commercial purposes but only for personal use.


## Pokedex
- :negative_squared_cross_mark: Nordvpn 
- :interrobang: Linkedin 
- :interrobang: Yelp
- :interrobang: Youporn
- :interrobang: Pornhub
- :ballot_box_with_check: Netflix
- :ballot_box_with_check: Uplay

  
## Requirements
- [MariaDB](https://mariadb.org/)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- Pip packages listed in [requirements.txt](requirements.txt)

## Common issues
- You might have some errors installing **mysqlclient package**. In our case [this](https://github.com/facebook/prophet/issues/418) solved our problems.

## Setup environment
To setup the entire environment necessary to start testing your functions you must follow these steps:
 1) Running the mariadb daemon;
 2) Create an user and give him permission to modify the entire db or just create a database for a better permission control;
 3) Configure the file [.config.ini](.config.ini) with the local and remote mariadb user. A prompt will ask every single key that must be used
 4) Use the file [test.py](test.py) to test a single credentials, or [main.py](main.py) to test the entire in db to every single function in the Pokedex. 
 
## How to contribute 
You must follow these steps to contribute to this project:
 1) Satisfy all requirements listed in the [Requirements section](#requirements);
 2) Follow the steps listed in [Setup Environment section](#setup-environment);
 3) Choose to test websites that aren't in the pokedex yet or complete an uncompleted website (fix function, add test...);
 4) Create a branch called "website_name" and checkout that branch (push in master branch is blocked);
 5) Define/modify a function in  [functions.py](functions.py);
 6) Test that function individually using [test.py](test.py);
 7) Once the function is complete and doesn't crash the software, you can open a pull request.  
