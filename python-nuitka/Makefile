
hello-world:
	python3 -m nuitka --standalone --onefile --follow-imports --show-progress --output-dir=dist hello_world.py

fastapi:
	python3 -m nuitka --standalone --onefile --follow-imports --show-progress --output-dir=dist fastapi_example.py

.PHONY: clean
clean:
	rm -fr dist *.xml
