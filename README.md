# CatchEmAll
![Docker Image CI](https://github.com/0ssigeno/CatchEmAll/workflows/Docker%20Image%20CI/badge.svg)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

The aim of this project is to test random credentials found in data dumps. 
Precisely every credential, which is saved on a db, is used to test access in all the websites listed in [Pokedex section](#pokedex). 
  
## Warning
This software can't be used for commercial purposes but only for personal use.


## Pokedex
- :negative_squared_cross_mark: Nordvpn 
- :negative_squared_cross_mark: Spotify
- :ballot_box_with_check: Linkedin 
- :ballot_box_with_check: Yelp
- :ballot_box_with_check: Youporn
- :ballot_box_with_check: Pornhub
- :ballot_box_with_check: Netflix
- :ballot_box_with_check: Uplay

  
## Requirements
- [MariaDB](https://mariadb.org/)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [TOR](https://2019.www.torproject.org/docs/debian.html.en)
- Pip packages listed in [requirements.txt](requirements.txt)


## Setup environment
 1) Please use the [dockerfile](Dockerfile) provided to have a stable environment
 2) Use the file [test.py](test.py) to test your single user and password, or [main.py](main.py) to test the entire in db to every single function in the Pokedex. 
 
## How to contribute 
You must follow these steps to contribute to this project:
 1) Satisfy all requirements listed in the [Requirements section](#requirements);
 2) Follow the steps listed in [Setup Environment section](#setup-environment);
 3) Choose to test websites that aren't in the pokedex yet or complete an uncompleted website (fix function, add test...);
 4) Create a branch called "website_name" and checkout that branch (push in master branch is blocked);
 5) Create a new entry in [PokedexCatching](PokedexCatching) with the site that you are going to test;
 6) Test that function individually using [test.py](test.py);
 7) Once the function is complete and doesn't crash the software, you can open a pull request.  
