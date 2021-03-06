#!/usr/bin/env python
"""
    Small example of interaction with Moscow Exchange ISS server.

    Version: 1.1
    Developed for Python 2.6

    Requires iss_simple_client.py library.
    Note that the valid username and password for the MOEX ISS account
    are required in order to perform the given request for historical data.

    @copyright: 2016 by MOEX
"""

from iss_simple_client import Config
from iss_simple_client import MicexAuth
from iss_simple_client import MicexISSClient
from iss_simple_client import MicexISSDataHandler

#My imports
import sys
import datetime
import csv
#json to read config file
import json
import pandas as pd
#My import ends
            
class MyData:
    """ Container that will be used by the handler to store data.
    Kept separately from the handler for scalability purposes: in order
    to differentiate storage and output from the processing.
    """

    def __init__(self):
        self.history = []

    def print_history(self):
        for sec in self.history:
            print sec

    def print_history_tofile(self):
        with open(outfile,'ab') as resultFile:
            wr = csv.writer(resultFile, delimiter='\t')
            wr.writerows(self.history)
    
    # inspired by github.com/pdevty/googlefinance-client-python/blob/master/googlefinance
    def as_dataframe(self):
        index = []
        data = []
        for sec in self.history:
            index.append(sec[0])
            data.append([sec[2],sec[3],sec[4],sec[5],sec[6]])
        return pd.DataFrame(data, index = index, columns = ['Open', 'High', 'Low', 'Close', 'Volume']) 
            
class MyDataHandler(MicexISSDataHandler):
    """ This handler will be receiving pieces of data from the ISS client.
    """
    def do(self, market_data):
        """ Just as an example we add all the chunks to one list.
        In real application other options should be considered because some
        server replies may be too big to be kept in memory.
        """
        self.data.history = self.data.history + market_data

def get_price_data(ticker, days_befoure):
    """Get current day's data and display print it on screen."""
    #config_file=raw_input('config file: ')
    config_file="d:/tmp/moex.json"    
    try:
        with open(config_file) as config_file:    
            conn_data = json.load(config_file)
    except:
        print "Error: Unable to read config file. "
        sys.exit(1)

    username = conn_data['username']
    password = conn_data['password']
    my_config = Config(user=username, password=password, proxy_url='')

    my_auth = MicexAuth(my_config)
    date = datetime.datetime.now() - datetime.timedelta(days_befoure)
    
    #ticker = 'SBER' # for tesing...
    
    if my_auth.is_real_time():
        iss = MicexISSClient(my_config, my_auth, MyDataHandler, MyData)
        iss.get_history_securities('stock',
                                   'shares',
                                   'tqbr',
                                   ticker, 
                                   date.strftime("%Y-%m-%d")
                                   #here to be start end dates
                                   )
        #print iss.handler.data.history
    return iss.handler.data.as_dataframe() 
        
if __name__ == '__main__':
    try:
        get_price_data('SBER', 30)
    except:
        print "Sorry:", sys.exc_type, ":", sys.exc_value
