docker_img:
	docker build --tag text-summarizer-img .

docker_container:
	docker run --name TextSummarizer -p 4000:8900 text-summarizer-img