from matplotlib import pyplot as plt
import argparse

def plot_route_1(points):
	for i in range(len(points)-1):
		if i == 0:
			plt.plot([points[i][0], points[i+1][0]],[points[i][1], points[i+1][1]], 'ro-')
		else:
			plt.plot([points[i][0], points[i+1][0]],[points[i][1], points[i+1][1]], 'ro--')
	plt.plot([points[0][0], points[-1][0]],[points[0][1], points[-1][1]], 'ro--')
	plt.plot(points[0][0], points[0][1], 'bo')
	plt.title("Blue node is starting node. Solid line is first move.")
	plt.savefig("route.png", bbox_inches='tight')

	plt.show()

def read_data(fname):
	points = []
	domain = -1
	with open(fname, 'r') as f:
		for i, l in enumerate(f.readlines()):
			if i == 0:
				domain = int(l)
			else:
				if domain == 1:
					l = l.split(",")
					points.append((int(l[0]), int(l[1])))
				else:
					pass
	f.close()
	return points, domain

def main(args):
	points, domain = read_data(args.datafile)
	print("domain: ", domain)
	if domain == 1:
		plot_route_1(points)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('datafile')
	main(parser.parse_args())