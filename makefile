domain1-single:
	python assign2_1.py -t 0 locations.txt
	python graph.py output.txt
domain1-minute:
	python assign2_1.py -t 60 locations.txt
	python graph.py output.txt
