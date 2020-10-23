build:
	flit build

# ensure this passes before commiting
check:
	black --check nxp_dlagent
	isort --check nxp_dlagent
	flake8 nxp_dlagent

fix:
	black nxp_dlagent
	isort nxp_dlagent

all: UM11126 blhost_2.6.2 elftosb_5.1.19

UM11126:
	./nxp-dl UM11126

blhost_2.6.2:
	./nxp-dl blhost_2.6.2

elftosb_5.1.19:
	./nxp-dl elftosb_5.1.19

venv:
	virtualenv venv
	pip install -U pip selenium

check:
	black --check nxp_dlagent
	isort --check nxp_dlagent
	flake8 nxp_dlagent

fix:
	black nxp_dlagent
	isort nxp_dlagent
