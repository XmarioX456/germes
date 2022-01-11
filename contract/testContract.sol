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

contract gg {

   address WBNB;
   address pancakeRouterAddress;

   constructor() {
        WBNB = 0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd;
        pancakeRouterAddress = 0xD99D1c33F9fC3444f8101754aBC46c52416550D1;
   }
   receive() payable external {}

   event log(address[] pair, address receiver, uint256 amountIn);

   function swap(address[] calldata path, uint256 amountIn) external payable {  
      address[] memory tempPath = new address[](2);
      address receiver;

      if (path[0]!=WBNB) {
         //IBEP20(path[0]).transferFrom(msg.sender, address(this), amountIn);
      } else {
         amountIn = msg.value;
      }

      for (uint8 i=0; i<path.length-1; ++i) {
         tempPath[0] = path[i];
         tempPath[1] = path[i+1];
         if (i != path.length-2) {
            receiver = address(this);
         } else {
            receiver = msg.sender;
         }
         if (tempPath[0] == WBNB) {
         } else if (tempPath[1] == WBNB) {
         } else {
         } 
         emit log(tempPath, receiver, amountIn);
      }
   }
   
   function multyswap(address[] calldata path, uint256 amountIn) external payable {
      
      address[] memory tempPath = new address[](2);
      address receiver;

      if (path[0]!=WBNB) {
         IBEP20(path[0]).transferFrom(msg.sender, address(this), amountIn);
      } else {
         amountIn = msg.value;
      }


      for (uint8 i=0; i<path.length-1; ++i) {
         tempPath[0] = path[i];
         tempPath[1] = path[i+1];
         if (i != path.length-2) {
            receiver = address(this);
         } else {
            receiver = msg.sender;
         }
         if (tempPath[0] == WBNB) {
            IPancakeRouter01(pancakeRouterAddress).swapExactETHForTokens{value: amountIn}( 
               0,
               path,
               receiver,
               block.timestamp + 100
            );
            amountIn = IBEP20(tempPath[1]).balanceOf(address(this));
         } else if (tempPath[1] == WBNB) {
            IBEP20(tempPath[0]).approve(pancakeRouterAddress, amountIn);
            IPancakeRouter01(pancakeRouterAddress).swapExactTokensForETH(
               amountIn,
               0,
               tempPath,
               receiver,
               block.timestamp + 100
            );
            amountIn = address(this).balance;
         } else {
            IBEP20(tempPath[0]).approve(pancakeRouterAddress, amountIn); 
            IPancakeRouter01(pancakeRouterAddress).swapExactTokensForTokens(
               amountIn,
               0,
               tempPath,
               receiver,
               block.timestamp + 100
            );
            amountIn = IBEP20(tempPath[1]).balanceOf(address(this));  
         }

      } 
   }

}