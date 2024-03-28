// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

contract Iot {
    // Mapping to store string data by a unique identifier
    mapping(uint256 => string) public iotdata;

    // Counter to generate unique identifiers for each string record
    uint256 public iotcounter;

    // Address that is authorized to store IoT data
    address public authorizedAddress;

    // Modifier to restrict access to the storeIotdata function
    modifier onlyAuthorized() {
        require(msg.sender == authorizedAddress, "Unauthorized access");
        _;
    }

    // Constructor to set the authorized address
    constructor() public {
        authorizedAddress = msg.sender;
    }

    // Function to store string data, only accessible by the authorized address
    function storeIotdata(string calldata data) external onlyAuthorized {
        // Increment the counter to get a unique identifier
        iotcounter++;

        // Store the string data in the mapping with the unique identifier
        iotdata[iotcounter] = data;
    }

    // Function to retrieve string data by identifier
    function getIoTdata(uint256 iotId) external view returns (string memory) {
        // Retrieve the string data by the provided identifier
        return iotdata[iotId];
    }

    // Function to get the value of iotcounter
    function getIotCounter() external view returns (uint256) {
        return iotcounter;
    }
}

