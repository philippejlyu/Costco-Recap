# Getting receipt data
Go to costco.ca and select orders and returns.

In the dropdown menu for showing, you will need to select January to June and July to December
In your network inspector, this will create 2 files named graphql. This is the json formatted data for each receipt

Save these 2 files as a .json and rename the files in the files array on line 39 appropriately.

Note that this only gives us item numbers which is not very interesting

# Getting item descriptions from item numbers
In the future this will be done with selenium however at this time I am doing this manually.

Whenever you click view receipt, another graphql file is created in the network inspector

Save these files in the Receipts directory.

You can do this for each receipt, however you should be able to get your top 10 items by sampling them instead.