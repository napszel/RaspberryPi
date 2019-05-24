#!/bin/bash

# Price eth_tmp and btc_tmp random nevu file nevvel kell letre hozni tmp file utility.
# a python program ezutan os.exec-el hivhatja ezt a programot internetrol toltes helyett
set -e

date=$(date +%Y%m%d)

# Download ETH and BTC prices to file
curl -f -g -s 'https://api.coinmarketcap.com/v1/ticker/ethereum/' > price_eth_tmp.json || echo Downloading ETH prices failed
curl -f -g -s 'https://api.coinmarketcap.com/v1/ticker/bitcoin/' > price_btc_tmp.json || echo Downloading BTC prices failed

# Delete the []
sed -i '$ d' price_eth_tmp.json
sed -i '1,1d' price_eth_tmp.json
sed -i '$ d' price_btc_tmp.json
sed -i '1, 1d' price_btc_tmp.json

mv price_eth_tmp.json price_eth.json
mv price_btc_tmp.json price_btc.json




