setup:
	pip install -r requirements.txt
	cp apikeys.template apikeys.py
	
clean:
	rm -f unsplash.jpg sample_presentation.pptx
	rm -rf presentations/*