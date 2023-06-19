docker_img:
	docker build --tag text-summarizer-img .

docker_container:
	docker run --name TextSummarizer -p 8550:8550 text-summarizer-img