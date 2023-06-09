---
title: Cryptography 
tags:
- programming
- technology
image: /images/crypto/info.png
---

In parallel with those Azure courses I'm also taking a 7 week course on cryptography from the university of Maryland on Coursera. Let's begin.

<!--more-->

[Github repository of my code for this course](https://github.com/vandanrohatgi/Cryptography)

# Week 1

Classic cryptography assumed that both parties shared a common secret which can be used to encrypt and decrypt the message. This was known as Private key crypto/ secret key/ shared key/symmetric-key cryptography. This shared key is assumed to be secret.

<img src="/images/crypto/privatekey.png">

`<-` or `->` will be used for random algorithm. meaning the one giving different output for same input. `:=` is used for deterministic algos. Which means the algo will give the same output on the same inputs.

Decrypt(k,Encrypt(k,msg))=msg

## Shift Cipher

<img src="/images/crypto/shift.png">

k is the key which can either be represented as 0,1,2... or a,b,c...

Every letter of the message will be shifted towards right. For Decryption it will be shifted towards left.

Some notations for later in the course.

<img src="/images/crypto/modular.png">

25=35 Mod 10 (Because both 25 and 35 have same remainder when divided by 10)
25!=[35 Mod 10] (Because [35 Mod 10]=5)

shift cipher does not handle upper case, numbers or special characters.

<img src="/images/crypto/formalshift.png">

Shift cipher is not secure because it has only 26 keys. So a normal bruteforce on the key will work successfully.

Kerckhoff's principle states that the algorithm used for encrytption should not be a secret but the key used should be.

<img src="/images/crypto/kerck.png">

Key space should be large enough so that brute force doesn't work.

## Vigenere Cipher

Here we use a phrase instead of a single alphabet key to encrypt.

![](/images/crypto/vigen.png)

Here the key is "cafe" and message is "tell him about me". 

The Vigenere cipher was considered secure for many years because:
- keys can be 26 characters long, for ex if key is 14 chars long then just the key space is 2^66. not counting the bruteforce that has to be performed with each key.

One of attacks discussed in the course is frequency attack where we use the plain text letter frequencies which is just a diagram showing the most used alphabets in english language.

![](/images/crypto/freq.png)

I read a bit more about this attack and concluded that it was too much for my pea sized brain. The gist that I was able to get was that we take the alphabets that are found the most in english then we assume that the cipher is also having those same alphabets as the most repeated. We then perform further analysis, we find the length of the key and I blacked out after this.

In the end I would like to say that the vigenere cipher can be broken and it's not secure. Thank you for coming to my TED talk. Moving on...

## Hex and ASCII

in Decimal system we use 10 numbers to represent data and in Hexadecimal we use 16. 0-9 and then A-F.

![](/images/crypto/hex.png)
![](/images/crypto/convert.png)

Types of threat models of encryption:
1. cipher only attack: the attacker just has access to the cipher text. it can be dangerous if a hacker gets his hand on multiple cipher texts.
2. known plain text: the attacker know the plain text behind the cipher.
3. chosen plain text attack: the plain text that is affected by the attacker
4. chosen cipher text attack


[comment]: <> (My main priority is to learn about common cryptography algorithms. The programming assignments were just making it hard to be focussed on that goal. I will try to come back to them In the end. Also, I just realized that I'm just copying and pasting the course slides and I find the theory of this course boring. I will be continuing with the basic algorithms from this course over my github repo. [Here's the link again](https://github.com/vandanrohatgi/Cryptography))


