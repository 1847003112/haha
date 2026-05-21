import string
import random
def mi():
    n=string.ascii_letters + string.digits
    b=''.join([random.choice(n) for i in range(6)])
    return b