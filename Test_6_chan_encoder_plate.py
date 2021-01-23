from Robogaia import Encoder6
import time

encoders = Encoder6()

# Main Program starts here
encoders.InitializeEncoders()

for i in range(0, 10000):
    values = []
    for i in range (1, encoders.max):
       values.append(encoders.ReadEncoder(i))
    print(values)
    time.sleep(0.10)

encoders.Cleanup()
