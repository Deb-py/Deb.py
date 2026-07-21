def ball_to_over(ball):
	over = f'{int(ball/6)}.{int(ball%6)}'
	return over
def over_to_ball(over):
	ball = (10*over) - (4*int(over))
	return int(ball)
print(ball_to_over(45))
print(over_to_ball(18.3))