all: build/pkg

build/pkg: clean
	@mkdir -p build/pkg
	@cp main.py build/pkg/
	@cd build && touch miniplay
	@cd build && echo "/usr/bin/env python" >> miniplay
	@cd build/pkg && zip -r ../pkg.zip *
	@cd build && cat pkg.zip >> miniplay
clean:
	rm -rf build

