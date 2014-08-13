all: build/pkg

build/pkg: clean
	@mkdir -p build/pkg
	@cp -a src/* build/pkg/
	@echo "from server import daemonize;daemonize()" > build/pkg/__main__.py
	@cd build && touch miniplay
	@cd build && echo "/usr/bin/env python" >> miniplay
	@cd build/pkg && zip -r ../pkg.zip *
	@cd build && cat pkg.zip >> miniplay
	@cd build && chmod +x miniplay
clean:
	rm -rf build

