PHONY: all

src/LeM.out:
	@echo "I need LeM.out executable in ${PWD}/src/"
	@exit 1

Input/LeM_input.txt:
	@echo "I need LeM_input.txt executable in ${PWD}/Input/"
	@exit 1

all: src/LeM.out
	bokeh serve .
