pragma solidity 0.8.0;

//import "https://github.com/pancakeswap/pancake-swap-periphery/blob/master/contracts/interfaces/IPancakeRouter01.sol";
//import "https://github.com/binance-chain/bsc-genesis-contract/blob/master/contracts/interface/IBEP20.sol";

interface IBEP20 {
    function totalSupply() external view returns (uint256);
    function decimals() external view returns (uint8);
    function symbol() external view returns (string memory);
    function getOwner() external view returns (address);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address _owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

interface IPancakeRouter01 {
   function swapExactETHForTokens(
      uint amountOutMin,
      address[] calldata path,
      address to,
      uint deadline
   )
      external
      payable
      returns (uint[] memory amounts);

   function swapExactTokensForETH(
      uint amountIn,
      uint amountOutMin,
      address[] calldata path,
      address to,
      uint deadline
   )
      external
      returns (uint[] memory amounts);

   function swapExactTokensForTokens(
      uint amountIn,
      uint amountOutMin,
      address[] calldata path,
      address to,
      uint deadline
   )
      external
      returns (uint[] memory amounts);

   function getAmountsOut(
      uint amountIn,
      address[] calldata path
   )
      external
      view
      returns (uint[] memory amounts);

   function getAmountsIn(
      uint amountOut,
      address[] calldata path
   )
      external
      view
      returns (uint[] memory amounts);
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

   function multiswap(uint256 amountIn, address[] calldata path) external payable returns (uint8[] memory) {
      require(isUser(msg.sender), "Germes: ACCESS_DENIED");
      /*if (path[0] == WBNB) {
         
      } else {
         IBEP20(path[0]).transferFrom(msg.sender, address(this), amountIn);
      }*/
      uint8[] memory testresult;
      for (uint i = 0; i < path.length; ++i) {
         address token0 = path[i];
         address token1 = path[i+1];
         address[2] memory ticker = [token0, token1];
         if (token0 == WBNB) {
            testresult[i] = 1;
         } else if (token1 == WBNB) {
            testresult[i] = 2;
         } else {
            testresult[i] = 3;
         }
         return testresult;

      }
   }

   /*function swapBNBForToken(address token1) external payable {
      address[] memory path = new address[](2);
      path[0] = WBNB;
      path[1] = token1;
      IPancakeRouter01(0xD99D1c33F9fC3444f8101754aBC46c52416550D1).swapExactETHForTokens{value: msg.value}(
         0,
         path,
         msg.sender,
         10000000000
      );
   }*/

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