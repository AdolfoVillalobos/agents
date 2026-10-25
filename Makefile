.DEFAULT_GOAL := help
.PHONY: help install install-no-rtk adhd-on-demand test-install

help: ## Muestra los comandos disponibles
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  make %-16s %s\n", $$1, $$2}'

install: ## Módulos de skills + ADHD siempre activo + RTK
	./install.sh

install-no-rtk: ## Igual que install, sin instalar ni configurar RTK
	./install.sh --skip-rtk

adhd-on-demand: ## Igual que install, con i-have-adhd solo bajo demanda (/i-have-adhd)
	./install.sh --no-adhd-always-on

test-install: ## Prueba la instalación en directorios aislados, sin modificar tus agentes
	python3 -m unittest discover -s tests -v
