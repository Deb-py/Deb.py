import cmath

def qut_sol(equ):
	a, b, c = 0, 0, 0
	equ = equ.replace("x^2", "x²").replace("x2", "x²").replace(" ", "")
	equ = equ.replace("-", "+-").split("+")
	for i in equ:
		if not i:
			continue
		elif "x²" in i:
			if i.replace("x²", "") == "" or i.replace("x²", "") == "-":
				a += float(i.replace("x²", "1"))
			else:
				a += float(i.replace("x²", ""))
		elif "x" in i:
			if (i.replace("x", "") == "") or (i.replace("x", "") == "-"):
				b += float(i.replace("x", "1"))
			else:
				b += float(i.replace("x", ""))
		else:
			c += float(i)
			
	a = int(a) if a == int(a) else a
	b = int(b) if b == int(b) else b
	c = int(c) if c == int(c) else c
	
	cequ = ((f"{a}x²" if a != 0 else "") + (f"+{b}x" if b != 0 else "") + (f"+{c}" if c != 0 else "")).replace("+-", "-")
	
	if a == 0:
		if b == 0:
			return 'No variable To solve'
		lans = -c/b
		return f"{cequ} --> x = {int(lans) if lans == int(lans) else lans}", a, b, c, cequ
			
	else:
		d = cmath.sqrt(b**2 - 4*a*c)
		root1 = (-b + d)/(2*a)
		root2 = (-b - d)/(2*a)
		try:
			root1 = int(root1) if root1 == int(root1) else root1
			root2 = int(root2) if root2 == int(root2) else root2
		except:
			nothing = "nothing"
				
	factor = f"(x+{-root1})(x+{-root2})".replace("+-", "-").replace("(x-0)", "x").replace("(x+0)", "x")
				
	return f"{cequ} --> x = {root1:.2f}, x = {root2:.2f}  \nfactor = {factor}", a, b, c, cequ, root1, root2, factor

# ENTER QUADRATIC EQUATION 👇🏻

equation = 'x2+4'

print(qut_sol(equation)[0])


equations = ['x²+  7x+12', 'x2-x', 'x^2-4', '-x2+5x+6', '7x + x² + 12', 'x²+5x', 'x²-2x-3']