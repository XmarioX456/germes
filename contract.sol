pragma solidity ^0.8.7;

contract germesContract {

   address owner;
   address[] users;

   constructor() {
      owner = msg.sender;
      users.push(owner);
   }

   function isUser(address _address) public view returns (bool) {
      for (uint i = 0; i < users.length; ++i) {
         if (users[i] == _address) {
            return true;
         }
      }
      return false;
   }

   function transferOwnership(address newOwner) external {
      require(msg.sender == owner, "GERMES: ACCESS_DENIED");
      owner = newOwner;
   }

   function addUser(address _address) external {
      require(msg.sender == owner, "GERMES: ACCESS_DENIED");
      users.push(_address);
   }

   function delUser(address _address) external {
      require(msg.sender == owner, "GERMES: ACCESS_DENIED");
      for (uint i = 0; i < users.length; ++i) {
         if (users[i] == _address) {
            delete users[i];     
         }
      }
   }

   function multiswap(uint256 amountIn, address[] calldata path) external {
      require(isUser(msg.sender), "GERMES: ACCESS_DENIED");
      for (uint i = 0; i < path.length; ++i) {
         address token1 = path[i];
         address token2 = path[i+1];
         //swap();
      }
   }

   function getOwner() external view returns (address) {
      return owner;
   }

   function getUsers() external view returns (address [] memory) {
      return users;
   }

   function balance() external view returns(uint256) {
      return address(this).balance;
   }

   function destroy(address payable to) public {
      require(msg.sender == owner, "GERMES: ACCESS_DENIED");
      selfdestruct(to);
   }

   function recieve() external payable {}

}