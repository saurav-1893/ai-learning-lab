import sys
import os

if len(sys.argv) < 2:
    sys.exit('Please provide a CSV file')
    
elif not os.path.isfile(sys.argv[1]):
    sys.exit('File not found')
print(sys.argv)