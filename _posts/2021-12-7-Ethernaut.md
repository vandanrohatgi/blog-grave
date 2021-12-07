---
title: Ethernaut Writeups 
tags:
- technology
- blockchain
image: /images/ether/info.png
---

Starting my the second phase of my blockchain security journey [First one here](https://github.com/vandanrohatgi/Unga-Bunga-Coin). Now that I know a little bit of how blockchains work I wanted to dive straight into it's security aspect.

<!--more-->

Some may say I still don't know many things about blockchain, how will I ever secure it? That's the beauty of top-down learning. You learn as you go. It's not the typical routine of learn the thoery and then get the hand dirty. I beleive in learning on the job. With that out of the way... Lets dive into my first solve.

# Hello Ethernaut

[Play along](https://ethernaut.openzeppelin.com/level/0x4E73b858fD5D7A5fc1c3455061dE52a53F35d966)

So first we just follow the basic setup guide, which is pretty clear. We interact with the challenges using the web console in our browsers. Here is where some might face trouble. The link provided in the guide to get test ether (which is required to play) does not work. [Here is an alternative I found](https://faucets.chain.link/rinkeby). It only gives 0.1 Ether, but that much is enough to play these challenges.

Also if cant call the "player" or "ethernaut" functions and variables, try opening the console and refreshing the page. Starting the challenge. It is pretty easy since this is just an example challenge. The challenge said to look into contract.info() to start.

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
