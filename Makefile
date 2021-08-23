PYTHON	= python
PYDOC	= pydoc
PYCS	= $(shell find . -name "*.pyc")
PYCACHE	= $(shell find . -name "__pycache__")
FILES   = $(shell basename `find . -name "*.py"`)
ARCHIVE	= $(shell basename `pwd`)
TARGET	= main.py
MODULE	= main
WORKDIR	= ./codes/
PYLINT	= pylint
LINTRCF	= .pylintrc
LINTRST	= pylintresult.txt
REQUIRE = requirements.txt
REFORMAT = black

all:
	@:

wipe: clean
	@find . -name ".DS_Store" -exec rm {} ";" -exec echo rm -f {} ";"
	(cd ../ ; rm -f ./$(ARCHIVE).zip)

clean:
	@for each in ${PYCS} ; do echo "rm -f $${each}" ; rm -f $${each} ; done
	@for each in ${PYCACHE} ; do echo "rm -f $${each}" ; rm -rf $${each} ; done
	@if [ -e $(LINTRST) ] ; then echo "rm -f $(LINTRST)" ; rm -f $(LINTRST) ; fi

test:
	$(PYTHON) $(WORKDIR)$(TARGET)

doc:
	$(PYDOC) $(WORKDIR)$(TARGET)

zip: wipe
	(cd ../ ; zip -r ./$(ARCHIVE).zip ./$(ARCHIVE)/ --exclude='*/.svn/*')

pydoc:
	(sleep 3 ; open http://localhost:9999/$(MODULE).html) & $(PYDOC) -p 9999

lint: modules clean reformat
	@if [ ! -e $(LINTRCF) ] ; then $(PYLINT) --generate-rcfile > $(LINTRCF) 2> /dev/null ; fi
	@for each in $(FILES); \
	do \
		$(PYLINT) --rcfile=$(LINTRCF) $(WORKDIR)$${each} >> $(LINTRST); \
	done; \
	less $(LINTRST);

#
# pip is the PyPA recommended tool for installing Python packages.
#
pip:
	@if [ -z `which pip` ]; \
	then \
		(cd $(WORKDIR); curl -O https://bootstrap.pypa.io/get-pip.py); \
		(cd $(WORKDIR); sudo -H python get-pip.py); \
		(cd $(WORKDIR); rm -r get-pip.py); \
	else \
		(cd $(WORKDIR); sudo -H pip install -U pip); \
	fi

#
# requirements.txtに書き込まれているモジュールのうち、含まれていないモジュールの一括インストールを行う
#
modules: pip
	@for each in $(shell cat $(REQUIRE)); \
	do \
		if [ -z `pip list --format=freeze | grep $${each}` ]; \
		then \
			(cd $(WORKDIR); sudo -H pip install $${each}); \
		fi \
	done

#
# List of the required packages
#
list: pip
	@(pip list --format=freeze | grep pip)
	@for each in $(shell cat $(REQUIRE)); \
	do \
		if [ -z `pip list --format=freeze | grep $${each}` ]; \
		then \
			(echo $${each} not found); \
		else \
			(sudo -H pip list --format=freeze | grep $${each}); \
		fi \
	done

prepare: modules

update: modules

reformat: modules
	@for each in $(FILES); \
	do \
		(cd $(WORKDIR); $(REFORMAT) $${each}); \
	done \
