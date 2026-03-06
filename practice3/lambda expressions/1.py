numbers=[2,4,6,8,10]
def square(numbers):
    sq_numbers=list(map(lambda x:x*x,numbers))
    return sq_numbers
print(square(numbers))