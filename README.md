# Invited customers

Invite customers within 100km from office to a party. The GPS coordinates for our office are 53.339428, -6.257664.

## Description
This program reads a full list of customers and outputs the names and user ids of matching customers (within 100km), sorted by 
user id (ascending). 

Customer records are provided in a text file (customers.txt) -- one customer per line, JSON lines formatted. 

To calculate distance - https://en.wikipedia.org/wiki/Great-circle_distance. 

Note that degrees are converted to radians.
