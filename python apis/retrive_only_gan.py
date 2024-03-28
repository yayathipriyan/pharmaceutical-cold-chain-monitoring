from web3 import Web3
import time
import json
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("Connected to Ganache")
else:
    print("Failed to connect to Ganache. Make sure it's running.")

contract_address = "0x8B63a5Bf3C79Db53377dF64d0115637F0c64B957" 
contract_abi = [
	{
		"constant": True,
		"inputs": [],
		"name": "iotcounter",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"name": "iotdata",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "authorizedAddress",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getIotCounter",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "iotId",
				"type": "uint256"
			}
		],
		"name": "getIoTdata",
		"outputs": [
			{
				"name": "",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "data",
				"type": "string"
			}
		],
		"name": "storeIotdata",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "constructor"
	}
]

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)






account = web3.eth.accounts[0]  # Replace with your account
web3.eth.defaultAccount = account
a=35.0
b=165
while(1):
    temperature_to_store = '{\"temp\":'+str(a)+','+'\"humidity\":'+str(b)+'}'
    a=a+2.3
    b=b+1.32
    transaction_hash = contract.functions.storeIotdata(temperature_to_store).transact({'from': account, 'gas': 200000})
    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Transaction receipt: {transaction_receipt}")

    iot_counter_value = contract.functions.getIotCounter().call()
    print("Current value of iotcounter:", iot_counter_value)
     
     

    iot_counter_value = contract.functions.getIotCounter().call()
    temperature_record_id = iot_counter_value  # Replace with the desired temperature record ID
    r= contract.functions.getIoTdata(temperature_record_id).call()
    print(f"Retrieved temperature: {r}")
    print(type(r))
   
    r.replace("'",'"')
    print(r)
    time.sleep(5)

iot_counter_value = contract.functions.getIotCounter().call()
print("Current value of iotcounter:", iot_counter_value)
     
     

    







# Interact with the smart contract Retrieve temperature data
