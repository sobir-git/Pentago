class Board():
	ind = {}
	for i, j in ((1, 1), (1, 4), (4, 1), (4, 4)):
		normal1 = ((i-1, j), (i, j+1), (i+1, j), (i, j-1))
		normal2 = ((i-1, j+1), (i+1, j+1), (i+1, j-1), (i-1,j-1))
		rev1 = tuple(reversed(normal1)) 
		rev2 = tuple(reversed(normal2)) 
		ind[(i, j)] = ((rev1, rev2), (normal1, normal2))

	def empty_array(self,array=None):
		if not array:
			self.array = [[None]*6 for _ in range(6)]
		else:
			self.array = array

	def __init__(self, array=None):
		if array is None:
			self.empty_array()
		else:
			self.array = array

	def rotate(self, i, j, clockwise):
		a = self.array
		for ind in self.ind[(i, j)][clockwise]:
			xor, yor = ind[0]
			prev = a[xor][yor]
			for x, y in ind:
				now = a[x][y]
				a[x][y] = prev
				prev = now
			a[xor][yor] = prev

	def print(self):
		p = lambda el: "%2s" % (el if el is not None else '.')
		res = []
		for row in self.array:
			res.append(''.join(map(p, row)))
		res = '\n'.join(res)
		print(res)

	def __hash__(self):
		return hash(self.array)


def test_rotate():
	from pprint import pprint
	b = Board()
	i, j = 4, 4
	b.array[i][j] = 8
	for n, (x, y) in enumerate(((i-1, j), (i-1, j+1), (i, j+1), (i+1, j+1), (i+1, j), (i+1, j-1), (i, j-1), (i-1,j-1))):
		b.array[x][y] = n
	print("before roatation:")
	b.print()
	b.rotate(i, j, True)
	print("after roatation:")
	b.print()


if __name__ == '__main__':
	test_rotate()
