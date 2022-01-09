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

   function multiswap(uint256 amountIn, address[] calldata path) external payable {

      require(isUser(msg.sender), "Germes: ACCESS_DENIED");
      if (path[0] == WBNB) {
         require(amountIn == msg.value, "Germes: INVALID_INPUT");
      } else {
         IBEP20(path[0]).transferFrom(msg.sender, address(this), amountIn);
      }

      for (uint i = 0; i < path.length; ++i) {
         address token0 = path[i];
         address token1 = path[i+1];
         address[] memory shortPath = new address[](2);
         shortPath[0] = path[i];
         shortPath[1] = path[i+1];
         address receiver;
         uint256 amountOut;

         if (i == path.length-1) {
            receiver = msg.sender;
         } else {
            receiver = address(this);
         }
         if (i == 0) {
            amountOut = amountIn;
         }

         if (token0 == WBNB) {
            amountOut = IPancakeRouter01(pancakeRouterAddress).swapExactETHForTokens{value: msg.value}(
               0,
               shortPath,
               receiver,
               block.timestamp + 100
            )[0];

         } else if (token1 == WBNB) {
            IBEP20(token0).approve(pancakeRouterAddress, amountOut);
            amountOut = IPancakeRouter01(pancakeRouterAddress).swapExactTokensForETH(
               amountOut,
               0,
               shortPath,
               receiver,
               block.timestamp + 100
            )[0]; 

         } else {
            IBEP20(token0).approve(pancakeRouterAddress, amountOut);
            amountOut = IPancakeRouter01(pancakeRouterAddress).swapExactTokensForTokens(
               amountOut,
               0,
               shortPath,
               receiver,
               block.timestamp + 100
            )[0];
         }

      }
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

   function swapTokenForBNB(address token0, uint256 amount) external {
      IBEP20(token0).transferFrom(msg.sender, address(this), amount);
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