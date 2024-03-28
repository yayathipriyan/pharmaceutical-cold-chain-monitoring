import requests
from bs4 import BeautifulSoup
import time
from web3 import Web3
i=1


while(1):
    url = "http://192.168.159.192"  # Replace this with the URL you want to fetch
    t=""
    h=""
    d=""
    ti=""
    response = requests.get(url)

    if response.status_code == 200:
        html_data = response.text
        #print(html_data)
        soup = BeautifulSoup(html_data, 'html.parser')
        t = soup.find('p',id='temp')
        h = soup.find('p',id='humi')
        d = soup.find('p',id='date')
        ti= soup.find('p',id='time')
        print("Data : ",i)
        i=i+1
        print("========================================")
        print(t.text)
        print(h.text)
        print(d.text)
        print(ti.text)
        print("========================================")
        
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
    time.sleep(2)
    

    #data= '{\"time\":'+str(ti.text)+','+'\"date\":'+str(d.text)+','+'\"temperature\":'+str(t.text)+','+'\"humidity\":'+str(h.text)+'}'
    #data= '{\"date\":'+str(d.text)+','+'\"time\":'+str(ti.text)+','+'\"temperature\":'+str(t.text)+','+'\"humidity\":'+str(h.text)+'}'
    ti=str(ti.text)
    ti=ti.replace(":","/")
    temperature_to_store = '{\"date\":'+'"'+str(d.text)+'"'+','+'\"time\":'+'"'+str(ti)+'"'+','+'\"temperature\":'+'"'+str(t.text)+'"'+','+'\"humidity\":'+'"'+str(h.text)+'"'+'}'
    #temperature_to_store = '{\"date\":'+str(536.2)+','+'\"time\":'+str(85.3)+','+'\"temperature\":'+str(t.text)+','+'\"humidity\":'+str(h.text)+'}'
    print(type(ti))
    print(temperature_to_store)
    print(type(temperature_to_store))
    ganache_url = "http://127.0.0.1:7545"  # Update with your Ganache URL
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    if web3.is_connected():
      print("Connected to Ganache")
    else:
      print("Failed to connect to Ganache. Make sure it's running.")

    # Replace with your contract address and ABI
    contract_address = "0x8B63a5Bf3C79Db53377dF64d0115637F0c64B957"  # Update with your contract address
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

    # Interact with the smart contract
    account = web3.eth.accounts[0]  # Replace with your account
    web3.eth.defaultAccount = account
    #transaction_hash = contract.functions.storeTemperature(temperature_to_store).transact()
    #transaction_hash = contract.functions.storeTemperature(temperature_to_store).transact({'gas': 200000})


   
    
    transaction_hash = contract.functions.storeIotdata(temperature_to_store).transact({'from': account, 'gas': 200000})
    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Transaction receipt: {transaction_receipt}")
    iot_counter_value = contract.functions.getIotCounter().call()
    # Retrieve temperature data
    temperature_record_id =iot_counter_value
    print(temperature_record_id)
    # Replace with the desired temperature record ID
    retrieved_temperature = contract.functions.getIoTdata(temperature_record_id).call()
    print(f"Retrieved temperature: {retrieved_temperature}")

    #delay 5 seconds
    time.sleep(5)





