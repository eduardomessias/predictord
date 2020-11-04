# Predictord

Stock trading strategies using Python

In the scope of enriching beyond the possibilities hidden in the financial market, a graphical analysis tool appears capable of predicting the best moments of buying and selling the papers existing on the American stock exchange.

Actually, what you see are graphs based on widely known analyzes, such as SMA and MACD, produced in a web application created to practice my web-development skills.

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
