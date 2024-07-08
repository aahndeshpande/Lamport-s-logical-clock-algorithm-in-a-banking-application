# Lamport-s-logical-clock-algorithm-in-a-banking-application


Problem Statement :
Implement Lamport’s logical clock algorithm in a banking application based on gRPC that mimics interactions between customer and branches in a distributed system. Banking application has numerous financial procedures, including deposits, withdrawals, balance queries, and money transfers, must be handled by the system.

Goal :
The goal in the problem statement is to implement Lamport’s logical clock algorithm
1.Implement logical clock in every customer and branch process
2. Implement Lamport’s algorithm for clock coordination among the processes
3. The logical clock should be local to each branch. logical clock is not shared by branches.


How to run the project : - 
step 1 - Run python Branch.py input_10.json
step 2 - Run python Customer.py input_10.jso
step 3 - Interrupt the Branch file for output 2 (ctrl +C)
note delete all the output before running branch and customer.py file


Implementation Processes :-

In the grpc banking application we implemented lamports logical clock according to the request sent and request received.
For customer -
•
Every consumer keeps track of occurrences using a logical clock.
•
The logical clock is increased by actions like deposits, withdrawals, and inquiries.
•
To make event ordering easier, messages are forwarded to branches with the logical clock included.
For branch –
•
Each branch maintains its logical clock to timestamp events.
•
Events received from customers are assigned logical timestamps based on Lamport's Logical Clock.
•
Propagation events (e.g., propagate_deposit , propagate_withdraw) also update the logical clock.
For message delivery-
•
Messages exchanged between customers and branches include logical clocks.
•
Logical clocks are used to establish the order of events during processing.
•
Messages sent between branches for event propagation also carry logical clocks.

Results :- 
we have 3 output files :
1.
In ouput1 file we have the List of all the events taken place on each customer
2.
In output 2 we have list of all events that takes place on each branch we get ouput after stopping the branch file
3.
In output 3 we have List of all the events and with their logical times triggered by each customer Deposit/Withdraw request
Overall implementation of Lamport’s logical clock algorithm was successful.
