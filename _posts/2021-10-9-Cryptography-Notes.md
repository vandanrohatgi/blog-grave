---
title: Cryptography 
tags:
- programming
- technology
image: /images/crypto/info.png
---

In parallel with those Azure courses I'm also taking a 7 week course on cryptography from the university of Maryland on Coursera. Let's begin.

<!--more-->

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