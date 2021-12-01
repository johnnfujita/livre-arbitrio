# __Crypto Pipe__

## Description
A simple pipeline to access multiple crypto exchanges, then; 

- Clean and normalize data from the multiple sources;
- Store data
- Perform analisys and decision;
- Trigger actions;
- Gather post-mortem intelligence;


____

## Modules:

### 1. APIs Integrations (e.g.) Binance api, Bybit api:

Each exchange has its own submodule divided into:

### - Data Reading:

Basically read data from the exchange e.g.:ticks,account balance;

The data reads will be consumed by independent api data fetchs within a controlled interval;

Websockets are available, but due to the lack of support for some exchanges and simplicity, we will postpone its implementation.

maybe later we may breakdown into a separate microservice for each api

### - Actions:
    
Any call that mutates the user account state e.g:transfers, withdraw, short, long.
    
### 2. Data Processing:

A simple module that unifies the diverse data model structures from each API into a single normalized data structure. Multiple Data Views can be generated here but the main one has the following equivalent the following format (python syntax):

A dict with the keys: 

- event_time (timestamp); 

- bids: 
    
    Inner dict with symbols as keys and the respective values are lists of 2 tuples contaning exchange name and the value for highest and lowest bids for each symbol; 

- asks:

    Inner dict with symbols as keys and the respective values are lists of 2 tuples contaning exchange name and the value for lowest and highest asks for each symbol;

```python
{   "event_time": 324324234, # utc timestamp
    
    # dicts of bids for each coin (descending)
    "bids": {
        # list with a pair of tuple (highest and lowest bids for the given symbol)
        "COIN1_NAME": [("exchange_highest_bider_name", 10000),("exchange_lowest_bider_name", 1)],
        # list with a pair ... for the second symbol
        "COIN2_NAME": [("exchange_highest_bider_name", 10000),("exchange_lowest_bider_name", 1)],
        # nth symbol
    },
    
    # dict of asks for each coin (ascending) 
    "asks": {
        # list with a pair of tuple (lowest and highest asks for the given symbol)   
        "COIN1_NAME": [("exchange_lowest_asker_name", 1),("exchange_highest_asker_name", 10000)],
        # list with a pair ... for the second symbol
        "COIN2_NAME": [("exchange_lowest_asker_name", 1),("exchange_highest_asker_name", 10000)],
        # ... nth symbol
    }
}


```

### 3. Storage:

Since trading data can be easilly found from specialized websites, storing long term data doesn't present major benefits, although we may opt for a custom model that may better fit our needs.

But anyway, some storage is important and short term in memory storage to perform time series analysis is of the most importance. So we will at least keep the last 24h data in memory. 

The last 6 min will be probably the most important for arbitrage, cause it is the time that takes to perform a on block transfer (BTC transfer min time)

The fastest storage is Feather although we may not notice any significant benefit on the scale we are working on.


### 4. Analysis and Decision:

This module is the intelligence of the system, it will use data science and machine learning methods to achieve success in any given strategy defined by user

### __Available strategies:__

- Arbitrage
    - This strategy aims to compare live prices and respective volumes of a given asset across all exchanges, already considering the time to fulfill all the required assets flow and taking into account all the fees involved.



### 5. Post-Mortem:

This module is responsible for retrospectively examining all actions and decisions taken by the system. To give light for possible further improvements.   

## Usage

The program is not that flexible yet, it doesn't aim for a high level of user interaction. Although some customizations may be added as the system matures.


1. initialize the environment, in this directory run:  

``` shell
$ virtualenv -p <your-python-version> env

$ source env/bin/activate

```

2. install the dependecies:

```
$ pip install -r requirements

```

3. run the code to start the bot:

```
$ python main.py --strategy arbitrage --mode action

```

4. to check the cumulative results from the bot decision on a given strategy:

```
$ python main.py --strategy arbitrage --mode post-mortem

```