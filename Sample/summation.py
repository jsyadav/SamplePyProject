'''
Created on Feb 6, 2015

@author: jyadav
'''
# summation.py
# Compute the sum of the first 100 integer values and print
# the results.

# Initialize a constant variable.
NUM_VALUES = 100

# Compute the sum.
summation = 0
i = 1
while i <= NUM_VALUES:
    summation = summation + i
    i = i + 1

# Print the results.
print "The sum of the first", NUM_VALUES, \
      "integers is", summation
 
