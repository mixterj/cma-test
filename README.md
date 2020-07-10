# CMA Developer Test
This is a simple Python Flask Web Application that creates an interactive gallary of 100 sample pieces of art from the Cleveland Museum of Art. The application requires the building of a JSON file prior to running the web application. The interactive gallary provides general browsing, detailed viewing of items, faceting by Department and Creator, and simple search.

## Requirements
* Python3
* Python3 Flask library
* Python3 Flask Boostrap library
* Python3 sqlite3 library

## Install
1. install [Python3](https://www.python.org/downloads/)
2. install PIP3
3. install Flask library
  * `sudo pip3 install flask`
4. install Flask Boostrap library
  * `sudo pip3 install flask-bootstrap`
5. install sqlite3 library
  * `sudo pip3 install sqlite3`

## Deployment
1. clone github repo
  * `git clone https://github.com/mixterj/cma-test.git`
2. navigate to the 'cma-test/static/scripts/' directory and run the 'process_sql/py' script
 * `cd cma-test/static/scripts/`
 * `python3 process_sql/py`
3. navigate to the 'cma-test' root directory and run the 'app.py' script
 * `python3 app.py`
4. view the app in the browser on port 5001
 * `http://localhost:5001/`
