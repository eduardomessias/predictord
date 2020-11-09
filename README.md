# Predictord

Stock trading strategies using Python

In the scope of enriching beyond the possibilities hidden in the financial market, a graphical analysis tool appears capable of predicting the best moments of buying and selling the papers existing on the American stock exchange.

Actually, what you see are graphs based on widely known analysis, such as SMA and MACD, produced in a web application created to practice my web-development skills.

As I learn how to add other solid stock price analysis methods to the tool, new commits will come.

## References
Stock market visual analysis tool made in [Python](https://www.python.org/) using [Flask](https://flask.palletsprojects.com/en/1.1.x/).

The API [yfinance](https://pypi.org/project/yfinance/) is providing the stock info for this tool.

## Project layout
    predictord
    |- instance/
    |- src/
        |- static/
            |- style.css
        |- templates/
            |- predictord/
            |   |- index.html
            |- base.html
        |- __init__.py
        |- predictord.py
    |- venv/
    |- setup.py
    |- MANIFEST.in
    |- README.md

## Requirements

- Python 3.8
    - pip  
    - virtualenv

## How to run

1. Clone or download the main branch in this repo.
    1.1 If you download, unzip the downloaded file right after.
2. In a terminal app, change directory to the predictord downloaded folder.
```
$ cd predictord
```
3. Activate the virtual environment
```
$ . venv/bin/activate
```
4. Set FLASK_APP and FLASK_ENV variables
```
$ export FLASK_APP=src
$ export FLASK_ENV=development
```
6. Run the application
```
$ flask run
```
