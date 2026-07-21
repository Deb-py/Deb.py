import random
import time

high = 10
low = 0
x = random.randint(low, high)
high_nums = [high+1]
low_nums = [low-1]
print(f"> Guess the Number ({low} - {high})")

while True:
	y = int(input("\n> Your Guess :- "))
	if x > y:
		print("Higher ! ⬆️")
		low_nums.append(y)
	elif x < y:
		print("Lower ! ⬇️")
		high_nums.append(y)
	elif x == y:
		print("🎉 You Win ! 🎉")
		break
		
	com = random.randint(max(low_nums)+1, min(high_nums)-1)
	print("Computer is guessing...")
	time.sleep(1)
	print(f"> Computer Guess :- {com}")
	if x > com:
		print("Higher ! ⬆️")
		low_nums.append(com)
	elif x < com:
		print("Lower ! ⬇️")
		high_nums.append(com)
	elif x == com:
		print("🎉 Computer Win ! 🎉")
		break