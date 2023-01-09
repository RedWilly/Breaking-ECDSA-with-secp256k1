# Import necessary libraries
import hashlib
import time
import psutil

# Define the public key
p = "c477f9f65c22cce20657faa5b2d1d8122336f851a508a1ed04e479c34985bf96"

# Divide the public key into two subkeys
s1 = p[:len(p)//2]
s2 = p[len(p)//2:]

# Get the current CPU usage
cpu_usage = psutil.cpu_percent()

# Create an empty dictionary to store the results of the first subproblem
results1 = {}

# Solve the first subproblem by trying all possible values for the first half of the key
print("Solving first subproblem...")
for i in range(2**(len(s1)*8)):
  # Hash the current value and store the result in the dictionary
  results1[hashlib.sha256(i.to_bytes(len(s1), "big")).hexdigest()] = i
  print(f"Trying value {i} for s1...")

  # Check the CPU usage and sleep if necessary to use only 70% of the available processing power
  while psutil.cpu_percent() - cpu_usage > 70:
    time.sleep(120)

# Create a flag to track whether the secret key has been found
found = False

# Solve the second subproblem by trying all possible values for the second half of the key
print("Solving second subproblem...")
for i in range(2**(len(s2)*8)):
  # Hash the current value
  hash = hashlib.sha256(i.to_bytes(len(s2), "big")).hexdigest()
  print(f"Trying value {i} for s2...")

  # Check if the hash is in the dictionary from the first subproblem
  if hash in results1:
    # If the hash is in the dictionary, compute the hash of the full secret key
    key_hash = hashlib.sha256(results1[hash] + i).hexdigest()

    # Check if the hash of the full secret key is equal to the public key
    if key_hash == p:
      # If the hash of the full secret key is equal to the public key, we have found a solution!
      found = True
      key = results1[hash] + i
      break

  # Check the CPU usage and sleep if necessary to use only 70% of the available processing power
  while psutil.cpu_percent() - cpu_usage > 70:
    time.sleep(120)

# Print the result
if found:
  print(f"Secret key found: {key}")
else:
  print("Secret key not found")
