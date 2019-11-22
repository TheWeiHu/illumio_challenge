# Choice of Data Structure:

The total combinations of [direction] x [protocol] x [port] is small enough (262140) that I consider it reasonable to create a bucket for each of them.

However, since there is [255] x [255] x [255] x [255] possible ip addresses, I do not think it would not be reasonable to store every
[direction] x [protocol] x [port] x [ip] combination (~1.1E15 combinations).

Instead, I opted to store the ip addresses in their interval form. By storing them in sorted order, we can determine whether a packet satisfies the rules in O(logn) time, where n is the number of ip intervals for a given [direction] x [protocol] x [port] triple.

# Refinements:

Given more time, I would handle duplicated and overlapping rules. Instead of using bisect.insort(), I would need to write my own binary search and coalesce intervals.

E.g. adding (4, 5) to [(1,3), (6,7)] should produce [(1,7)]

I would also further test my code by adding more rules to the CSV file (especially ones involving large ranges, to see if any memory issues are introduced).

# Testing:

In addition to the tests provided, I included tests for my helper methods. I also added tests focusing on testing the rules' boundary cases.

# Miscellaneous:

When given a single port or ip address, I convert them into an interval.
e.g. 3000 becomes [3000, 3000]
This consistency helps with my implementation of binary search.

Also, I convert addresses into a tuple of 4 numbers, so that they can be easily compared.

# Teams:
Reading through the descriptions, there are problems worked on by all three teams that appeal to me.