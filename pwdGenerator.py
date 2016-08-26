from random import choice
import string

#Generate random passwords
def GenPasswd(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])    
      
if __name__ == '__main__':
    # Generate 10 random passwords
    for pwd in range(10):
        #Length of passwords is 8 digits
        print(GenPasswd(8))
        
