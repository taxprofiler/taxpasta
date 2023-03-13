################################################################################
# COMMANDS                                                                     #
################################################################################

.PHONY: qa
## Apply code quality assurance tools.
qa:
	isort src/taxpasta tests/ setup.py
	black src/taxpasta tests/ setup.py

.PHONY: docs
## Generate documentation
docs: qmd
	taxpasta standardise --help > docs/quick_reference/standardise_help.txt
	taxpasta merge --help > docs/quick_reference/merge_help.txt
	taxpasta consensus --help > docs/quick_reference/consensus_help.txt

snippets := $(patsubst %.qmd,%.md,$(wildcard docs/tutorials/*.qmd))

qmd: profiles $(snippets)

%.md: %.qmd
	quarto render $<

profiles: docs/tutorials/2612_pe-ERR5766176-db1_kraken2.tsv docs/tutorials/dbMOTUs_motus.tsv docs/tutorials/2612_pe-ERR5766176-db_mOTU.out docs/tutorials/2612_se-ERR5766180-db_mOTU.out docs/tutorials/2612_pe-ERR5766176-db1.kraken2.report.txt

docs/tutorials/2612_pe-ERR5766176-db1_kraken2.tsv: docs/tutorials/2612_pe-ERR5766176-db1.kraken2.report.txt
	cd docs/tutorials && taxpasta standardise -p kraken2 -o 2612_pe-ERR5766176-db1_kraken2.tsv 2612_pe-ERR5766176-db1.kraken2.report.txt

docs/tutorials/dbMOTUs_motus.tsv: docs/tutorials/2612_pe-ERR5766176-db_mOTU.out docs/tutorials/2612_se-ERR5766180-db_mOTU.out
	cd docs/tutorials && taxpasta merge -p motus -o dbMOTUs_motus.tsv 2612_pe-ERR5766176-db_mOTU.out 2612_se-ERR5766180-db_mOTU.out

docs/tutorials/2612_pe-ERR5766176-db_mOTU.out:
	cd docs/tutorials && curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/motus/2612_pe-ERR5766176-db_mOTU.out

docs/tutorials/2612_se-ERR5766180-db_mOTU.out:
	cd docs/tutorials && curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/motus/2612_se-ERR5766180-db_mOTU.out

docs/tutorials/2612_pe-ERR5766176-db1.kraken2.report.txt:
	cd docs/tutorials && curl -O https://raw.githubusercontent.com/taxprofiler/taxpasta/dev/tests/data/kraken2/2612_pe-ERR5766176-db1.kraken2.report.txt

################################################################################
# Self Documenting Commands                                                    #
################################################################################

.DEFAULT_GOAL := show-help

# Inspired by
# <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && \
		echo '--no-init --raw-control-chars')
