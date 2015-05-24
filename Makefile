SRV=bigdata
STATUS=lab6s_status.txt
GRAPH=data/graph.gpickle
RES=data/lab6sclustering.json

all: eval

eval:
	./evaluate.py $(GRAPH) $(RES)

load: 
	@scp $(RES) $(SRV):~

check:
	@ssh $(SRV) 'source .bash_profile && stat -c "%y" $(STATUS)  && cat $(STATUS)'