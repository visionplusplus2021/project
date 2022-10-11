
import subprocess
output = subprocess.getoutput("gpustat -P")
print(output)
