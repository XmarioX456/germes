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

   function WETH() external pure returns (address);

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
   address WETH;
   address routerAddress = 0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3;
   IPancakeRouter01 router = IPancakeRouter01(routerAddress);

   constructor() {
      owner = msg.sender;
      users.push(owner);
      WETH = router.WETH();
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

   function transferOwnership(address newOwner) external  {
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

   function multyswap(uint256 amountIn, address[] calldata path) external payable {
      if (path[0] == WETH) {
         require(amountIn == msg.value, "Germes: INVALID_INPUT");
      } else {
         IBEP20(path[0]).transferFrom(msg.sender, address(this), amountIn);
      }

      for (uint i = 0; i < path.length-1; ++i) {
         address receiver;
         address[] memory tempPath = new address[](2);

         tempPath[0] = path[i];
         tempPath[1] = path[i+1];

         if (i == path.length-2) {
            receiver = msg.sender;
         } else {
            receiver = address(this);
         }

         if (path[i] == WETH) {
            router.swapExactETHForTokens{value: msg.value}(
               0,
               tempPath,
               receiver,
               block.timestamp + 100
            );
            amountIn = address(this).balance;

         } else if (path[i+1] == WETH) {
            IBEP20(path[i]).approve(routerAddress, amountIn);
            router.swapExactTokensForETH(
               amountIn,
               0,
               tempPath,
               receiver,
               block.timestamp + 100
            );
            amountIn = IBEP20(tempPath[1]).balanceOf(receiver);

         } else {
            IBEP20(path[i]).approve(routerAddress, amountIn);
            router.swapExactTokensForTokens(
               amountIn,
               0,
               tempPath,
               receiver,
               block.timestamp + 100
            );
            amountIn = IBEP20(tempPath[1]).balanceOf(receiver);
         }
      }
   }

   function getOwner() external view returns (address) {
      return owner;
   }

   function getUsers() external view returns (address [] memory) {
      return users;
   }

   function balanceOf(address token) external view returns(uint256) {
      if (token == WETH) {
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