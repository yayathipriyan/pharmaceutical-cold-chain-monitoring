from web3 import Web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("Connected to Ganache")
else:
    print("Failed to connect to Ganache. Make sure it's running.")

contract_address = "0xFC138D1D260658c970C7ef2DD1B97D3aE19beE8C" 
contract_abi = [
	[
	{
		"constant": true,
		"inputs": [],
		"name": "iotcounter",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
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
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "authorizedAddress",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "getIotCounter",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
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
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "data",
				"type": "string"
			}
		],
		"name": "storeIotdata",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	}
]
]

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Interact with the smart contract
account = web3.eth.accounts[0]  # Replace with your account
web3.eth.defaultAccount = account

"""

# Store temperature data
temperature_to_store = "{temp:34.6;humidity:86}"
transaction_hash = contract.functions.storeIotdata(temperature_to_store).transact({'from': account, 'gas': 200000})
transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
print(f"Transaction receipt: {transaction_receipt}")


"""

# Retrieve temperature data
temperature_record_id = 1  # Replace with the desired temperature record ID
retrieved_temperature = contract.functions.getIoTdata(temperature_record_id).call()
print(f"Retrieved temperature: {retrieved_temperature}")

