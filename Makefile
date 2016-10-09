best:
	python -m kumonote.sandbox --config config/dos-attack.yaml
best2:
	python -m kumonote.sandbox --config config/dos-attack.yaml --override config/override/sample-requests2.yaml
best-limitted:
	python -m kumonote.sandbox --config config/dos-attack.yaml --override config/override/same-domain-limitter.yaml
worst:
	python -m kumonote.sandbox --config config/worst.yaml

result:
	rm -rf result
	mkdir -p result
	make best 2>&1 | tee result/best.txt &
	make best-limitted 2>&1 | tee result/best-limitted.txt &
	make worst 2>&1 | tee result/worst.txt &

.PHONY: result worst best
