db:
	docker-compose up -d db

rbmq:
	docker-compose up -d rbmq


test-all:
	just cerbes/test
	just aristaeus/test
	just hermes/test

run-all:
	alacritty -e just cerbes/serve &
	alacritty -e just aristaeus/serve  &
	alacritty -e just aristaeus/listen  &
	alacritty -e just hermes/listen  &
	alacritty -e just poseidon/serve  &

clean:
	kill $(ps u | grep -e 'just .*' | awk '{print $2}')
