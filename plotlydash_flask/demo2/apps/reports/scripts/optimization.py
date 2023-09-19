# This file is a Play ground for Trying diffeent opimization Techniques
import numpy as np
import time

# Numpy dot product
m1=np.random.randn(300,200)
m2=np.random.randn(200,500)


start= time.time()
result   = np.dot(m1,m2)
end = time.time()

print(f'Duration: {end-start} seconds')
