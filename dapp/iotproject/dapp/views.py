from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
import web3
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#1430
ganache_url = "HTTP://127.0.0.1:7545"

def login(request):
    #temp=loader.get_template("login.html")
    context={}
    return render(request,"login.html",context)



def check_address_in_network(address):
    try:
        w3 = web3.Web3(web3.Web3.HTTPProvider(ganache_url))
        accounts = w3.eth.accounts

        if address.lower() in [acc.lower() for acc in accounts]:
            return True
        else:
            return False

    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def homepage(request):
     return render(request,"homepage.html")


def processaddress(request):
    if request.method :
            ethereum_address = request.POST.get('ethereumAddress')
            isaddress=check_address_in_network(ethereum_address)
            if isaddress:
                context={}
                return render(request,"homepage.html",context)
            else:
                context={"data":"wrong"}
                return render(request,"login.html",context)
    
    else:
        data="Your address not found !!!!<br/> Enter correct address"
        context={
            "data":data,
        }
        return render(request,"login.html",context)
   

def Homepage(request):
     temp=loader.get_template("homepage.html")
     return HttpResponse(temp.render())

def showdata(request):
        parsed_data = Blockchain_data() 
        #parsed_data = [json.loads(item) for item in parsed_data]
        print(parsed_data)
        per_page = 10
        paginator = Paginator(parsed_data, per_page)
        page = request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        return render(request, 'mainpage.html', {'data': data})









def Mainpage(request):
    blockchain_data = Blockchain_data()
    parsed_data = blockchain_data
    print(parsed_data)
    temp=loader.get_template("mainpage.html")
    context={
          "data":parsed_data,
    }
   # return HttpResponse(temp.render(context,request))

    #return render(request, 'display_data.html', {'blockchain_data': blockchain_data})
    #return HttpResponse(blockchain_data)
    
     
    per_page = 10

    # Create a paginator object
    paginator = Paginator(parsed_data, per_page)

    # Get the current page number from the request
    page = request.GET.get('page')

    try:
        # Get the records for the requested page
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        data = paginator.page(paginator.num_pages)

    return render(request, 'mainpage.html', {'data': data})

    

























def Blockchain_data():
                ganache_url = "http://127.0.0.1:7545"
                web31 = web3.Web3(web3.Web3.HTTPProvider(ganache_url))

                if web31.is_connected():
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
                contract = web31.eth.contract(address=contract_address, abi=contract_abi)

                # Interact with the smart contract
                account = web31.eth.accounts[0]  # Replace with your account
                web31.eth.defaultAccount = account

                iot_counter_value = contract.functions.getIotCounter().call()
                print("Current value of iotcounter:", iot_counter_value)
                temperature_record_id = 1850
                data=[]

                for i in range(1850,iot_counter_value):
                    retrieved_temperature = contract.functions.getIoTdata(temperature_record_id).call()
                   # retrieved_temperature= con_dict(retrieved_temperature)
                    #t=json.loads(retrieved_temperature)
                    print(type(retrieved_temperature))
                    print(retrieved_temperature)
                    print(type(retrieved_temperature))
                    
                    data.insert(0,retrieved_temperature)
                    
                    temperature_record_id=temperature_record_id+1   
                #print(f"Retrieved temperature: {retrieved_temperature}")
                print(data)
                data = [json.loads(item) for item in data]
                print(data)
                return data


