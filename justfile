db:
	docker compose up -d db

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
	sudo kill -9 $(ps aux | grep -e 'just .*' | awk '{print $2}')
