# Warehouse stock - Python project
The sole purpose of this code is to 1) identify "fulfilled" and "unfulfilled" orders given an array of orderIds, and 2) identify when stock replenishment is required based on reaching a pre-defined stock threshold. As such, the code does not account for many edge cases which may be seen in a general business operation or production. Edge-cases and additional assumptions are highlighted throughout the code by comment.

## Main assumptions:
- The operator will only input unique orderIds

- Additional stock is not ordered for customer orders that could not be fulfilled (no backordering system exists). Effectively, the order becomes void and the customer must re-place the order when stock becomes available.

Pseudo code and comment has been added throughout to outline how a backorder system may be implemented, in-part.

## Additional information/running instructions:
- Run <pip3 install -r requirements.txt> in the project directory to install dependencies.
- Run file "process_orders.py"
- Await program response requesting user input.
- Additional stock and order reports may be found in the reports folder.