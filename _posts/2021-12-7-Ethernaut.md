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

# Introduction challenge

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