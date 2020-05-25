# pizero-fourletter-bitcoin
Bitcoin based scripts using the Pimoroni Four Letter pHAT on Raspberry Pi Zero

# Configuration
Configurable options are all set at the top of the script

## RPC Settings

When setting up, you will need to configure the RPC variables to point to your node.  Setting up a bitcoin node is outside of the scope of this project, but for those interested, check out the [RaspiBolt](https://github.com/Stadicus/RaspiBolt/) project. Make sure that in your bitcoin.conf, you have set server=1, and values for each of rpcuser, rpcpassword, rpcport, rpcbind, and rpcallowip. You'll need to modify your local network settings and firewall rules on the node you are connecting to in order to allow the RPC calls in.

- rpc_user - Assign the value you have for rpcuser in your bitcoin.conf file
- rpc_password - Assign the value you have for rpcpassword in your bitcoin.conf file
- rpc_host - The ip address or hostname of your bitcoin node, which may be the same as rpcbind in bitcoin.conf depending on your network setup.
- rpc_port - Assign the value you have for rpcport in your bitcoin.conf file

## Display Settings

There are multiple panels that may be displayed with scrolling messages.  You can toggle these on and off by setting the appropriate variable value to 1 or 0 respectively.

- show_welcome - Hardcoded string which you can easily alter and customize
- show_time - Network time in 24 hour format based on UTC. 
- show_temp - Current temperature of the CPU on the Raspberry
- show_price - Price of Bitcoin rounded to whole US Dollars.
- show_pricemsg - Provider message following the price
- show_blockheight - The blockheight your node sees
- show_mempoolsize - Mempool size for your node. This varies wildly amongst nodes based upon maxmempool in bitcoin.conf
- show_minfee - Current minimum fee in sats for a transaction to be accepted into the mempool

## Timing Settings

You can influence how long information is displayed before cycling to next panel, as well as how often the bitcoin node and price apis are queried

- minutes_between_api_updates - How often new price info and node information should be retrieved. Default of 5 minutes. This isn't meant to be a live second by second display of price as its a scroller. In general a few minutes between updates should be sufficient.  Some API providers indicate that they may rate limit, but no information was readily available to ascertain what their limits are, other than blockchain.info appears to provide 15 minute updates
- seconds_for_panel_display - How long, in seconds to pause before continuing to the next panel
- scrolling_speed - Higher values will scroll the text faster. Lower values will be slower.
