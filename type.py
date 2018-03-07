class Type(object):
	# Types ID:
	# int			->	1
	# double	->	2
	# char		->	3
	# bool		->	4
	# object	->	5
	# class		->	6
	# void		->	7

	def __init__(self, dimX, dimY, primType):
		self.dimX = dimX
		self.dimY = dimY
		self.primType = primType