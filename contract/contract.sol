pragma solidity 0.8.0;



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
   address pancakeRouterAddress;

   constructor() {
      owner = msg.sender;
      users.push(owner);
      WBNB = 0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd;
      pancakeRouterAddress = 0xD99D1c33F9fC3444f8101754aBC46c52416550D1;
   }

   receive() payable external {}

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

   event iterationLog(
      uint8 indexed i,
      uint[] indexed amounts

   );

   event stepLog(
      uint i
   );

   function multiswap(uint256 amountIn, address[] calldata path) external payable {
      emit stepLog(1);
      require(isUser(msg.sender), "Germes: ACCESS_DENIED");
      if (path[0] == WBNB) {
         require(amountIn == msg.value, "Germes: INVALID_INPUT");
      } else {
         IBEP20(path[0]).transferFrom(msg.sender, address(this), amountIn);
      }
      emit stepLog(2);

      for (uint i = 0; i < path.length-1; ++i) {
         address token0 = path[i];
         address token1 = path[i+1];
         address[] memory shortPath = new address[](2);
         shortPath[0] = path[i];
         shortPath[1] = path[i+1];
         address receiver;
         uint256 amountOut;
         uint[] memory result;

         if (i == path.length-2) {
            receiver = msg.sender;
         } else {
            receiver = address(this);
         }
         if (i == 0) {
            amountOut = amountIn;
         }

         if (token0 == WBNB) {
            result = IPancakeRouter01(pancakeRouterAddress).swapExactETHForTokens{value: msg.value}(
               0,
               shortPath,
               receiver,
               block.timestamp + 100
            );
            amountOut = result[1];

         } else if (token1 == WBNB) {
            IBEP20(token0).approve(pancakeRouterAddress, amountOut);
            result = IPancakeRouter01(pancakeRouterAddress).swapExactTokensForETH(
               amountOut,
               0,
               shortPath,
               receiver,
               block.timestamp + 100
            );
            amountOut = result[1];

         } else {
            IBEP20(token0).approve(pancakeRouterAddress, amountOut);
            result = IPancakeRouter01(pancakeRouterAddress).swapExactTokensForTokens(
               amountOut,
               0,
               shortPath,
               receiver,
               block.timestamp + 100
            );          
            amountOut = result[1];
         }

      }
   }

   function swap(uint256 amountIn, address[] calldata path) external payable { 
      require(path[0] == WBNB, "Germes: INVALID_ENTRY_POINT");
      address[] memory shortPath = new address[](2);
      shortPath[0] = path[0];
      shortPath[1] = path[1];
      IPancakeRouter01(pancakeRouterAddress).swapExactETHForTokens{value: msg.value}(
         0,
         shortPath,
         address(this),
         block.timestamp + 100
      );
   }


   function swapBNBForToken(address token1) external payable returns (uint[] memory) {
      address[] memory path = new address[](2);
      path[0] = WBNB;
      path[1] = token1;
      uint[] memory amounts = IPancakeRouter01(0xD99D1c33F9fC3444f8101754aBC46c52416550D1).swapExactETHForTokens{value: msg.value}(
         0,
         path,
         msg.sender,
         10000000000
      );
      return amounts;
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