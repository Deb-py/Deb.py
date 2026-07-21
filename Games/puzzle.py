import random 
import time

def change(txt):
	return list(txt[-1] + txt[0:-1])

def hint_pos(t_txt, f_txt):
	t_txt, f_txt = t_txt.replace(" ", ""), f_txt.replace(" ", "")
	hint, t_pos = "", []
	for i in range(len(t_txt)):
		if t_txt[i] == f_txt[i]:
			hint += "T "
			t_pos.append(i)
		else:
			hint += "F "
	return hint, t_pos

def com_turn(t_txt, r_chars):
	x = 0
	
	while True:
		x += 1
		c_chars = {}
		c_guess = " ".join(r_chars)
		#print(f"> {c_guess}")
		hint, pos = hint_pos(t_txt, c_guess)
		#print(f"> {hint}\n")
		if hint == "T "*len(r_chars):
			#print(f"  🎉 BOT Win in {x} guess 🎉\n")
			return x
		for i in reversed(pos):
			c_chars[i] = r_chars[i]
			r_chars.remove(r_chars[i])
		r_chars = change("".join(r_chars))
		c_chars = dict(sorted(c_chars.items()))
		for key in c_chars.keys():
			r_chars.insert(key, c_chars[key])
		#time.sleep(2)

def user_turn(t_txt):
	x = 0
	
	while True:
		x += 1
		inp = " ".join(input("> Enter your guess :- ").upper().replace(" ", ""))
		print(f"> {inp}")
		hint = hint_pos(t_txt, inp)[0]
		print(f"> {hint}\n")
		if hint == "T "*len(t_txt.replace(" ", "")):
			print(f"  🎉 YOU Win in {x} guess. 🎉\n")
			return x
		
def main():
	chars = list("ABCDEFG")
	r_chars = chars.copy()
	random.shuffle(chars)
	t_txt = " ".join(chars)
	
	print(f"> Guess the secret shuffle of -\n   {" ".join(r_chars)}\n")
	
	print("-------------- Your turn --------------")
	umg = user_turn(t_txt)
	
	print("-------------- Bot turn --------------")
	bmg = com_turn(t_txt, r_chars)
	
	if umg > bmg:
		print("> BOT Win .")
	elif umg < bmg:
		print("> YOU Win .")
	else:
		print("> It's DRAW .")
					
if __name__ == "__main__":
	main()