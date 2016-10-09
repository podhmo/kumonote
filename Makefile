best:
	python -m kumonote.sandbox config/dos-attack.yaml
worst:
	python -m kumonote.sandbox config/worst.yaml

result:
	rm -rf result
	mkdir -p result
	make best 2>&1 | tee result/best.txt &
	make worst 2>&1 | tee result/worst.txt &

.PHONY: result worst best
