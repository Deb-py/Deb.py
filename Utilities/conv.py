def dec2bs(num, base):
    hex_map = {10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
    x = int(num)
    base = int(base)
    if num == 0 or base <= 1:
        return "0"
    r_ans = ""
    while x != 0:
        x, ans = divmod(x, base)
        if ans > 9:
        	r_ans += hex_map[ans]
        else:
        	r_ans += str(ans)
    return r_ans[::-1]
    
def bs2dec(num, base):
	hex_map = {10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
	num = str(num)
	if num == "0" or base <= 1:
		return 0
	r_map = {v:k for k, v in hex_map.items()}
	bs = base
	result = 0
	ind = len(str(num))-1	
	for i in str(num):
		if not i.isdigit():
			i = r_map[i.upper()]
		result += int(i)*(bs**ind)
		ind -= 1
	return result

def conv(num, base, new_base):
	if base == new_base:
		return num
	elif base == 10:
		return dec2bs(int(num), int(new_base))
	elif new_base == 10:
		return bs2dec(num, int(base))
	else:
		return dec2bs(bs2dec(num, base), new_base)

def cal(num1, base1, sym, num2, base2, ans_base):
	if sym == "+":
		return dec2bs((bs2dec(num1, base1) + bs2dec(num2, base2)), ans_base)
	elif sym == "-":
		return dec2bs((bs2dec(num1, base1) - bs2dec(num2, base2)), ans_base)
	elif sym == "*":
		return dec2bs((bs2dec(num1, base1) * bs2dec(num2, base2)), ans_base)
	elif sym == "/":
		return dec2bs((bs2dec(num1, base1) / bs2dec(num2, base2)), ans_base)
	else:
		return ""

def main():
		
	print("1>>>- - - BASE CONVERTER - - -\n2>>>- - -     CALCULATION     - - -\n3>>>- - -           QUIT           - - -")
	while True:
		
		u_inp = input("Enter :- ")	
		
		if u_inp == "1":
			while True:	
				num = input("Enter Number :- ")
				base = int(input("Enter Base of this number :- "))
				new_base = int(input("Enter what base to convert :- "))
			
				print(f"{num}-{base} = {conv(num, base, new_base)}-{new_base}")
			
				if input("Enter 0 for back or 1 to redo :- ") == "0":
					break
					
		elif u_inp == "2":
			while True:
				num1 = input("Enter 1st number :- ")
				base1 = int(input("Enter base of 1st number :- "))
				sym = input("Enter +, -, *, / :- ")
				num2 = input("Enter 2nd number :- ")
				base2 = int(input("Enter base of 2nd number :- "))
				ans_base = int(input("Enter base of the ans :- "))
				print(f"{num1}-{base1} {sym} {num2}-{base2} = {cal(num1, base1, sym, num2, base2, ans_base)}-{ans_base}")
			
				if input("Enter 0 for back or 1 to redo :- ") == "0":
					break
				
		elif u_inp == "3":
			print("\n\n--- BAD BYE ---\n")
			break
				
if __name__ == "__main__":
	main()		