pragma solidity ^0.8.0;

contract Charity {
    struct Donation {
        address donor;
        uint256 amount;
        string recipient;
        string purpose;
        uint256 timestamp;
    }

    Donation[] public donations;
    mapping(address => uint256) public donorCounts;
    mapping(string => uint256) public recipientCounts;

    event DonationMade(address indexed donor, uint256 amount, string recipient, string purpose);

    function donate(string memory _recipient, string memory _purpose) public payable {
        require(msg.value > 0, "Donation amount must be greater than 0");
        
        donations.push(Donation({
            donor: msg.sender,
            amount: msg.value,
            recipient: _recipient,
            purpose: _purpose,
            timestamp: block.timestamp
        }));

        donorCounts[msg.sender]++;
        recipientCounts[_recipient]++;

        emit DonationMade(msg.sender, msg.value, _recipient, _purpose);
    }

    function getDonationCount() public view returns (uint256) {
        return donations.length;
    }

    function getDonation(uint256 _index) public view returns (address, uint256, string memory, string memory, uint256) {
        require(_index < donations.length, "Invalid donation index");
        Donation memory d = donations[_index];
        return (d.donor, d.amount, d.recipient, d.purpose, d.timestamp);
    }

    function getDonorCount(address _donor) public view returns (uint256) {
        return donorCounts[_donor];
    }

    function getRecipientCount(string memory _recipient) public view returns (uint256) {
        return recipientCounts[_recipient];
    }
}
