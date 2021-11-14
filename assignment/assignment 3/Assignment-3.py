
# coding: utf-8

# # Assignment 1: Functions
# 
# - Write a function ``assignment_01`` that multiplies an arbitrarily long list of number arguments (not passed as a list/collection but as single arguments)
# - Add some documentation
# 

# In[51]:


def assignment_01(*args):
    # your code here
    
    m = 1
    for number in args:
        m *= number
    
    return m


# # Assignment 2a: Loops 
# 
# - Write a function ``assignment_02_02a`` that expects a list with numbers
# - The function should initialize an empty list ``result`` and then iterate though the input list with a for loop
# - For each element of the input list, the function should add a string "higher" if the element was larger than 5 and "lower" otherwise
# - Then the list ``result`` should be returned by that function
# 

# In[52]:


def assignment_02a(numbers):
    result = []
    # your code here
    
    for number in numbers:
        result.append("higher") if number > 5 else result.append("lower")
            
    return result


# # Assignment 2b: List comprehensions
# 
# 
# - Now write a function ``assignment_02b`` that does the same in one line with list-comprehension
# 

# In[53]:


def assignment_02b(numbers):
    return ["higher" if n>5 else "lower" for n in numbers]


# # Assignment 3: Classes, Functions and Errors
# - Write a Class ``Duck``
# - A ``Duck`` constructor should accept variable length string arguments denoting the names of the duck
# - Internally the names are joined with a " " separator and stored as a single string in a field/attribute ``name``
# - A ``Duck`` has a function ``talks_to`` that 
#  - accepts one input argument 
#  - returns a string ``Quak`` if the input was another duck and raises a Value Error with the message "Can only talk to other Ducks" otherwise
#  - **Optional**: Create a function ``__repr__`` that prints the name of the Duck
# 

# In[54]:


class Duck:  
    def __init__(self, *args):
        self.name = " ".join([n for n in args])

    def talks_to(self, other_duck):
        
        if (not issubclass (type(other_duck), type(self))):
            raise ValueError("Can only talk to other Ducks")
        
        try:
            return 'Quak'
        except:
            return 'Error'
        
    def __repr__(self):
        return f"The name of the Duck is: {self.name}"


# # Tests
# 
# The cell below contains unit tests for your solution
# 
# Run the below cell (after running all the above cells with your code).
# 
# If there is no output/error when executing the tests, your code works.

# In[55]:


def assignment_01_test():
    assert assignment_01(1,2,3)==6

def assignment_02a_test():
    numbers = [1,6]
    assert assignment_02a(numbers)==['lower','higher']

def assignment_02b_test():
    numbers = [1,6]
    assert assignment_02b(numbers)==['lower','higher']

def assignment_03_test():
    duck = Duck("Alfred", "Judokus", "Quak")
    assert duck.name == 'Alfred Judokus Quak'

    other_duck = Duck("Hans", "Peter", "Schnabel")
    assert other_duck.name == 'Hans Peter Schnabel'
    assert duck.talks_to(other_duck) == "Quak"

    try:
        duck.talks_to("Crocodile")
    except ValueError as ve:
        assert str(ve) == "Can only talk to other Ducks"

assignment_01_test()
assignment_02a_test()
assignment_02b_test()
assignment_03_test()

