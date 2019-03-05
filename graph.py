from matplotlib import pyplot as plt
import argparse

def plot_route(points):
	for i in range(len(points)-1):
		if i == 0:
			plt.plot([points[i][0], points[i+1][0]],[points[i][1], points[i+1][1]], 'ro-')
		else:
			plt.plot([points[i][0], points[i+1][0]],[points[i][1], points[i+1][1]], 'ro--')
	plt.plot([points[0][0], points[-1][0]],[points[0][1], points[-1][1]], 'ro--')
	plt.plot(points[0][0], points[0][1], 'bo')
	plt.title("Blue node is starting node. Solid line is first move.")
	plt.show()
	plt.savefig("route.png")

def read_data(fname):
	points = []
	with open(fname, 'r') as f:
		for l in f.readlines():
			l = l.split(",")
			points.append((int(l[0]), int(l[1])))
	f.close()
	return points

def main(args):
	points = read_data(args.datafile)
	plot_route(points)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('datafile')
	main(parser.parse_args())