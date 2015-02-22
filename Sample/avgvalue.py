'''
Created on Feb 6, 2015

@author: jyadav
'''
# avgvalue.py
# Reads a group of positive integer values from the user,
# one at a time, until a negative value is entered. The average
# value is then computed and displayed.

# Initlize the counting variables.
total = 0
count = 0

# Extract the values.
value = int(raw_input("Enter an integer value (< 0 to quit): "))
while value >= 0 :
    total = total + value
    count = count + 1
    value = int(raw_input("Enter an integer value (< 0 to quit): "))
   
# Compute the average.
avg = float(total) / count

# Print the results.
print "The average of the", count, "values you entered is", avg
