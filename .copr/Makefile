srpm:
	rpmbuild \
		-bs \
		--define "_srcrpmdir $(outdir)" \
		--define "_sourcedir $(CURDIR)" \
		--undefine "dist" \
		$(spec)

