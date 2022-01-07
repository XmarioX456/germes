pragma solidity 0.8.2;

//import "https://github.com/pancakeswap/pancake-swap-periphery/blob/master/contracts/interfaces/IPancakeRouter01.sol";
//import "https://github.com/binance-chain/bsc-genesis-contract/blob/master/contracts/interface/IBEP20.sol";

interface IPancakeRouter01 {
   function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        payable
        returns (uint[] memory amounts);
}

interface IBEP20 {
   function balanceOf(address account) external view returns (uint256);
}

contract germesContract {

   address owner;
   address[] users;
   address WBNB;

   constructor() {
      owner = msg.sender;
      users.push(owner);
      WBNB = 0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd;
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
      require(msg.sender == owner, "Germes: ACCESS_DENIED");
      owner = newOwner;
   }

   function addUser(address _address) external {
      require(msg.sender == owner, "Germes: ACCESS_DENIED");
      users.push(_address);
   }

   function delUser(address _address) external {
      require(msg.sender == owner, "Germes: ACCESS_DENIED");
      for (uint i = 0; i < users.length; ++i) {
         if (users[i] == _address) {
            delete users[i];     
         }
      }
   }

   /*function multiswap(uint256 amountIn, address[] calldata path) external payable {
      require(isUser(msg.sender), "Germes: ACCESS_DENIED");
      if (path[0] == WBNB) {
         
      } else {
         IBEP20(path[0]).transferFrom(msg.sender, address(this), amountIn);
      }
      for (uint i = 0; i < path.length; ++i) {
         address token0 = path[i];
         address token1 = path[i+1];
         address[2] memory ticker = [token0, token1];

         //swap(0, );
      }
   }*/

   function swapBNBForToken(address token1) external payable {
      address[] memory path = new address[](2);
      path[0] = WBNB;
      path[1] = token1;
      IPancakeRouter01(0xD99D1c33F9fC3444f8101754aBC46c52416550D1).swapExactETHForTokens{value: msg.value}(
         0,
         path,
         msg.sender,
         block.timestamp + 100
      );
   }

   function getOwner() external view returns (address) {
      return owner;
   }

   function getUsers() external view returns (address [] memory) {
      return users;
   }

   function balanceOf(address token) external view returns(uint256) {
      if (token == WBNB) {
         return address(this).balance;
      } else {
         return IBEP20(token).balanceOf(address(this));
      }
   }

   function destroy(address payable to) public {
      require(msg.sender == owner, "Germes: ACCESS_DENIED");
      selfdestruct(to);
   }

}