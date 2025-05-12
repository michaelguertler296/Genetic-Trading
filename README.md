# Genetic Trading Algorithm for the S&P500

Instructions: Run the Main.py file

About: This project pulls economic data about from FRED (https://fred.stlouisfed.org/). Currently the project only uses daily closing data from the S&P500. The data is processed returning some basic economic features scaled down into a large data field. A genetic algorithm attempts to find the best combination of these economic features that maximize portfolio value. Signals are generated for each day between -1 (sell all stock for cash) and +1 (buy using all remaining cash). Results are plotted against a few different strategies including holding cash, dollar-cost-averaging, and buy-and-hold. 

Problems: 
1. The trades are super erratic (sell all, buy all)
2. Overfitting (will this work for future data?)

Future Work: 
1. Developing a really robust stock market simulation (so we can train and test this on different dates/time periods and to see realistic results)
2. Integrating larger sets of economic data (I could see Gold, VIX, BTC, Inflation, Unemployment giving meaningful data for the genetic algorithm to learn from/correlate to)
3. More accurate fitness function and signal function
