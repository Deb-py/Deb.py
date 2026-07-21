import random
import secrets
import string
sm_lat = string.ascii_lowercase
ca_lat = string.ascii_uppercase
num = string.digits
sym = string.punctuation
all = ca_lat + sm_lat + num + sym + " "
#all = "".join(chr(i) for i in range(1000))
def encode(pas, clst, rlst, w):
    random.seed(pas)
    random.shuffle(rlst)
    endct = dict(zip(clst, rlst))
    encode = ""
    for i in w:
        if i not in endct:
            return "Unexpected"
        elif i == " ":
            encode += endct[i]
            random.shuffle(rlst)
            endct = dict(zip(clst, rlst))
        elif i == "e":
            encode += endct[i]
            encode += secrets.choice(rlst)         
        else:
            encode += endct[i]
    return encode    
def decode(w, pas, c, r):
    random.seed(pas)
    random.shuffle(r)
    dedct = dict(zip(r, c))
    decode = ""
    sleep = False
    for i in w:
        if sleep == False:
            if i not in dedct:
                return "No! What?"
            elif dedct[i] == " ":            
                decode += dedct[i]
                random.shuffle(r)
                dedct = dict(zip(r, c))
            elif dedct[i] == "e":
                decode += dedct[i]
                sleep = True         
            else:
                decode += dedct[i]
        else:
            sleep = False
    return decode            
while True:
    cu_oder = list(all)
    ra_oder = list(all)
    a = input("<1> to Encode\n<2> to Decode\nEnter :  ")
    if a == "1":
        ewant = input("What to Encode ?\nEnter :  ")
        epas = input("Set a password ?\nEnter :  ")
        print(f"Encode : {encode(epas, cu_oder, ra_oder, ewant)}")
    elif a == "2":
        dwant = input("What to Decode ?\nEnter :  ")
        dpas = input("What is the password ?\nEnter :  ")
        print(f"Decode : {decode(dwant, dpas, cu_oder,ra_oder)}")