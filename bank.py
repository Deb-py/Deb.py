import json
try:
	with open("bank_data.json", "r") as f:
		accounts = json.load(f)
except:
	accounts = {}
print("---Bank Locker---")
_trump_un = "tariff250%"
_trump_pw = "china_modi"
while True:
	a = input("1. sign up or 2. log in :  ")
	if a == "1":
		new_un = input("Enter username :  ")
		if new_un in accounts:
			print("Username already exist, try another")
		else:
			new_pw = input("Enter password :  ")
			accounts[new_un] = {
			"password" : new_pw,
			"money" : 0,
			"mail" : []
			}
			print("Sign in successfull 🎉")
			with open("bank_data.json", "w") as f:
				json.dump(accounts, f)
	else:	
		un = input("Enter username :  ")
		pw = input("Enter password :  ")
		if un == _trump_un and pw == _trump_pw:
			print("Welcome to greenland mr duck 🦆")
			while True:
				x = input("What is the next noncence 1. see all acounts detail 2. see total money 3. to back :  ")
				if x == "1":
					for username, data in accounts.items():
						pw = data["password"]
						m = data["money"]
						print(f"UN {username} s PW is {pw} and have MONEY {m}$")
				elif x == "2":
					total_money = 0
					for username, data in accounts.items():
						total_money += data["money"]
					print(f"Total money for manipulation is {total_money}$")
				else:
					break
		elif un in accounts and accounts[un]["password"] == pw:
			print("Log in successfull 🎉 ")
			while True:
				y = input("Do you want to 1.  Check balance 2. Request for money 3. Send money 4. See mailbox 5. to back :  ")
				if y == "1":
					current = accounts[un]["money"]
					print(f"Your account balance is {current}$")
				elif y == "2":
					req = input("Enter sender username :  ")					
					if req == un:
						print("You can't send req to yourself ! 💦")
					elif req in accounts:
						if "mail" not in accounts[req]:
							accounts[req]["mail"] = []
						req_amount = int(input("How much request amount :  "))
						pac = {"sender" : un, "amo" : req_amount}
						accounts[req]["mail"].append(pac)
						print("Request sent successfully 🎉")
						with open("bank_data.json", "w") as f:
						    json.dump(accounts, f)
					else:
						print(f"User {req} don't exist ! 👎🏻")
				elif y == "3":
					terget = input("Who do you want to send :  ")
					if terget == un:
						print("You can't send money to yourself ! 🌚")
					elif terget in accounts:
						sm = int(input(f"How much money want to send to {terget} :  "))
						if accounts[un]["money"] >= sm:
							accounts[un]["money"] -= sm
							accounts[terget]["money"] += sm
							print("Money send successfully 💸")
							with open("bank_data.json", "w") as f:
								json.dump(accounts, f)
						else:
							print("Insufficient balance. stay in budget 🤡")
					else:
						print(f"Username {terget} don't exist 🚫")
				elif y == "4":
					print("---Mailbox---")
					m_mail = accounts[un]["mail"]
					if not m_mail:
						print("No mail ! 📬 ")
					else:
						for i, pac in enumerate(m_mail):
							s = pac["sender"]
							m = pac["amo"]
							print(f"Request #{i} : {s} is asking for {m}$")
						
						choice = input("Enter Request # to pay (or 'b' to back): ")
						
						if choice.isdigit():
							idx = int(choice)
							if idx < len(m_mail):
								# Pulling the info safely from the list
								bill = m_mail[idx]
								sender_un = bill["sender"]
								amount_to_pay = bill["amo"]

								if accounts[un]["money"] >= amount_to_pay:
									# Subtract from you, add to them
									accounts[un]["money"] -= amount_to_pay
									accounts[sender_un]["money"] += amount_to_pay
									
									# Remove the request from your mail
									m_mail.pop(idx)
									
									print(f"Paid {amount_to_pay}$ to {sender_un} 🎉")
									with open("bank_data.json", "w") as f:
										json.dump(accounts, f)
								else:
									print("Insufficient balance! 🆘")
							else:
								print("Invalid request number! 🚫")				
				else:
					break
		else:
			print("Incorrect password 🚧")