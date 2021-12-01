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

The data reads will be consumed by independent datasockets, maybe later we may breakdown into aseparate microservice for each api

### - Actions:
    
Any call that mutates the user account state e.g:transfers, withdraw, short, long.
    
### 2. Data Processing:

A simple module that unifies the diverse data model structures from each API into a single normalized data structure. Multiple Data Views can be generated here but the main one has the following equivalent json format

```json
{   
    "event_time": 324324234, // utc timestamp
    "binance": {
        "symbol":"BNBUSDT",     // symbol
        "top_bid":"25.35190000", // best bid price
        "top_bid_quantity":"31.21000000", // best bid qty
        "top_ask":"25.36520000", // best ask price
        "top_ask_quantity":"40.66000000"  // best ask qty
  
},
    "bybit": {
        "symbol":"BNBUSDT",     // symbol
        "top_bid":"25.35190000", // best bid price
        "top_bid_quantity":"31.21000000", // best bid qty
        "top_ask":"25.36520000", // best ask price
        "top_ask_quantity":"40.66000000"  // best ask qty
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

``` bash
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