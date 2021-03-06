domain1-single:
	python assign2.py -t 0 locations.txt
	python graph.py output.txt
domain1-half:
	python assign2.py -t 30 locations.txt
	python graph.py output.txt
domain1-minute:
	python assign2.py -t 60 locations.txt
	python graph.py output.txt
domain1-2min-20init:
	python assign2.py -t 120 -i 20 locations.txt
	python graph.py output.txt
domain1-10min-100init:
	python assign2.py -t 600 -i 100 -m 20 locations.txt
	python graph.py output.txt
domain2-single:
	python assign2.py -t 0 -d 2 towns.txt
	python graph.py output.txt
domain2-half:
	python assign2.py -t 30 -d 2 towns.txt
	python graph.py output.txt	
domain2-minute:
	python assign2.py -t 60 -d 2 towns.txt
	python graph.py output.txt