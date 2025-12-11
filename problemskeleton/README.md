# Kattis-ad-hoc-mathematical-puzzle-design
## Cyclic-prefix polydivisible numbers

### Words for Ari after our discussion
After our meeting, we got coding. But, we realized that we had one major problem with what we came up with together: 
Our initial goal was, as discussed:  
Given the number d1d2d3d4, we would work around the BigInt problem using the neat trick that modulo carries over:
d2d3 % b = (10*(d2 % b) + d3) % b  

But this had one major problem:  
The formula (d2d3 % b = (10*(d2 % b) + d3) % b) works when you are modding by the same b, but in our case, when we check the following digit, we are modding by b+1, which then loses all the commutative properties of modulo. 

So, instead, we developped the problem differently: we are still looping the modulo, i.e.: 1,2,....,9,10,1,2,....., but in order to check that the cyclic properties are satisfied we mod our prefix by 2520 (LCM of 1 to 10). Because this is the LCM of all moduli in the cycle, divisibility by any required m is preserved when the prefix is reduced modulo 2520. This is what we implement in our correct solution to maintain the carrying over of a smaller prefix, like we discussed. 

Happy reading! 
