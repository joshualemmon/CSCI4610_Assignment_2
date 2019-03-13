from matplotlib import pyplot as plt
import argparse

def plot_route_1(points, dist):
	for i in range(len(points)-1):
		if i == 0:
			plt.plot([points[i][0], points[i+1][0]],[points[i][1], points[i+1][1]], 'ro-')
		else:
			plt.plot([points[i][0], points[i+1][0]],[points[i][1], points[i+1][1]], 'ro--')
	plt.plot([points[0][0], points[-1][0]],[points[0][1], points[-1][1]], 'ro--')
	plt.plot(points[0][0], points[0][1], 'bo')
	plt.title("Total distance of path is " + str(dist))
	plt.savefig("route_domain_1.png", bbox_inches='tight')

	plt.show()

def plot_route_2(path, dist):
	label_to_city = {'A': "Brighton", 'B' : "Bristol", 'C' : "Cambridge", 'D': "Glasgow", 'E': "Liverpool", 'F' : "London", 'G' : "Manchester", 'H' : "Oxford"}
	legend = {"Brighton" : 'red', "Bristol" : 'blue', "Cambridge" : 'green', "Glasgow" : 'yellow', "Liverpool" : 'orange', "London": 'purple', "Manchester": 'pink', "Oxford" : 'brown'}
	coords = {"Brighton" : (70, 5), "Bristol" : (30, 30), "Cambridge" : (73, 80), "Glasgow" : (5, 250), "Liverpool" : (25, 130),
	                  "London": (70, 30), "Manchester": (40, 135), "Oxford" : (50, 40)}
	fig, ax = plt.subplots()
	plt.scatter(coords["Bristol"][0],coords["Bristol"][1], c=legend["Bristol"], label="Bristol")
	plt.scatter(coords["Brighton"][0],coords["Brighton"][1], c=legend["Brighton"], label="Brighton")
	plt.scatter(coords["London"][0],coords["London"][1], c=legend["London"], label="London")
	plt.scatter(coords["Cambridge"][0],coords["Cambridge"][1], c=legend["Cambridge"], label="Cambridge")
	plt.scatter(coords["Liverpool"][0],coords["Liverpool"][1], c=legend["Liverpool"], label="Liverpool")
	plt.scatter(coords["Manchester"][0],coords["Manchester"][1], c=legend["Manchester"], label="Manchester")
	plt.scatter(coords["Oxford"][0],coords["Oxford"][1], c=legend["Oxford"], label="Oxford")
	plt.scatter(coords["Glasgow"][0],coords["Glasgow"][1], c=legend["Glasgow"], label="Glasgow")
	ax.legend(bbox_to_anchor=(1.13, 1.15))
	path = list(path)
	title =''
	for i in range(len(path)):
		title += label_to_city[path[i]] + "-->"
		if i % 3 == 0 and i > 0:
			title +='\n'
		t1 = coords[label_to_city[path[i-1]]]
		t2 = coords[label_to_city[path[i]]]
		plt.plot([t1[0], t2[0]], [t1[1], t2[1]], color='black', linestyle='dashed')
	title = title[:-3]
	plt.title(title, fontsize='small')
	plt.xlabel("Total distance of path is " + str(dist))
	plt.savefig("route_domain_2.png", bbox_inches="tight")
	plt.show()
def read_data(fname):
	points = []
	path = None
	domain = -1
	with open(fname, 'r') as f:
		for i, l in enumerate(f.readlines()):
			if i == 0:
				domain = int(l)
			elif i == 1:
				dist = int(l)
			else:
				if domain == 1:
					l = l.split(",")
					points.append((int(l[0]), int(l[1])))
				else:
					path = l.strip('\n')
	f.close()
	return points, domain, dist, path

def main(args):
	points, domain, dist, path = read_data(args.datafile)
	print("domain: ", domain)
	if domain == 1:
		plot_route_1(points, dist)
	if domain == 2:
		plot_route_2(path, dist)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('datafile')
	main(parser.parse_args())