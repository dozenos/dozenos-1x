BUILDDIR=_build
VPATH=$(BUILDDIR)
OCAMLDIR=$(shell eval $$(opam env --root=/opt/opam --set-root); ocamlopt -where)
$(shell mkdir -p $(BUILDDIR) $(BUILDDIR)/stub $(BUILDDIR)/lib $(BUILDDIR)/stub_generator $(BUILDDIR)/test $(BUILDDIR)/generated)
PACKAGES=dozenos1x-config,vyconf.vyconfd-config,vyconf.vycall-client,re,ctypes.stubs,ctypes.foreign

GENERATOR_FILES=$(BUILDDIR)/lib/bindings.cmx \
                $(BUILDDIR)/stub_generator/generate.cmx

LIBFILES=$(BUILDDIR)/lib/bindings.cmx \
         $(BUILDDIR)/generated/dozenosconfig_bindings.cmx  \
         $(BUILDDIR)/lib/apply_bindings.cmx  \
         $(BUILDDIR)/generated/dozenosconfig.o

CAML_INIT=$(BUILDDIR)/stub/init.o
CAML_CTYPES:=$(shell eval $$(opam env --root=/opt/opam --set-root); ocamlfind query ctypes)
CAML_STDLIB:=$(shell eval $$(opam env --root=/opt/opam --set-root); ocamlfind ocamlc -config | awk '/^standard_library_default:/ {print $$2}')

# The files that we'll generate
GENERATED=$(BUILDDIR)/generated/dozenosconfig.h \
          $(BUILDDIR)/generated/dozenosconfig.c \
          $(BUILDDIR)/generated/dozenosconfig_bindings.ml

OSTYPE:=$(shell eval $$(opam env --root=/opt/opam --set-root); ocamlfind ocamlc -config | awk '/^os_type:/ {print $$2}')
SYSTEM:=$(shell eval $$(opam env --root=/opt/opam --set-root); ocamlfind ocamlc -config | awk '/^system:/ {print $$2}')
EXTDLL:=$(shell eval $$(opam env --root=/opt/opam --set-root); ocamlfind ocamlc -config | awk '/^ext_dll:/ {print $$2}')

CC:= $(shell eval $$(opam env --root=/opt/opam --set-root); ocamlfind ocamlc -config | awk '/^bytecomp_c_compiler/ {for(i=2;i<=NF;i++) printf "%s " ,$$i}')

LIBNAME:=libdozenosconfig.so.0

ifeq ($(OSTYPE),$(filter $(OSTYPE),Win32 Cygwin))
EXTEXE=.exe
else
EXTEXE=
endif

GENERATOR=$(BUILDDIR)/generate$(EXTEXE)

all: sharedlib

PHONY: depends
depends:
	sudo sh -c 'eval $$(opam env --root=/opt/opam --set-root) ;\
		opam pin add dozenos1x-config https://github.com/dozenos/dozenos1x-config.git#upstream-07636e49b3a04fdc76ac42bd65df88736c3945f1 -y ; \
		opam pin add vyconf https://github.com/dozenos/vyconf.git#upstream-ca209bc03badb1c344907e52803fbcd612f920a4 -y'

sharedlib: depends $(BUILDDIR)/libdozenosconfig$(EXTDLL)

ifeq ($(OSTYPE),$(filter $(OSTYPE),Win32 Cygwin))
$(BUILDDIR)/libdozenosconfig$(EXTDLL): $(CAML_INIT) $(LIBFILES)
	ocamlfind opt -o $@ -linkpkg -output-obj -verbose -package $(PACKAGES) $^
else ifeq ($(SYSTEM),$(filter $(SYSTEM),macosx))
$(BUILDDIR)/libdozenosconfig$(EXTDLL): $(CAML_INIT) $(LIBFILES)
	ocamlfind opt -o $@ -linkpkg -runtime-variant _pic -verbose -ccopt -dynamiclib -package $(PACKAGES) $^
else
$(BUILDDIR)/libdozenosconfig$(EXTDLL): $(CAML_INIT) $(LIBFILES)
	eval $$(opam env --root=/opt/opam --set-root); ocamlfind opt -o $@ -linkpkg -output-obj -runtime-variant _pic -verbose -thread -package $(PACKAGES) -ccopt "-Wl,-soname,$(LIBNAME)" $^
endif

stubs: $(GENERATED)

$(BUILDDIR)/stub/%.o:
	eval $$(opam env --root=/opt/opam --set-root); ocamlc -g -c stub/init.c
	mv init.o $@

$(GENERATED): $(GENERATOR)
	$(GENERATOR) $(BUILDDIR)/generated

$(BUILDDIR)/%.o: %.c
	$(CC) -c -o $@ -fPIC -I $(CAML_CTYPES) -I $(CAML_STDLIB) -I $(OCAMLDIR) -I $(OCAMLDIR)/../ctypes $<

$(BUILDDIR)/%.cmx: %.ml
	eval $$(opam env --root=/opt/opam --set-root); ocamlfind opt -c -o $@ -I $(BUILDDIR)/generated -I $(BUILDDIR)/lib -thread -package $(PACKAGES) $<

$(GENERATOR): $(GENERATOR_FILES)
	eval $$(opam env --root=/opt/opam --set-root); ocamlfind opt -o $@ -I $(BUILDDIR)/lib -linkpkg -thread -package $(PACKAGES) $^

install: sharedlib
	@mkdir -p /usr/lib
	@cp $(BUILDDIR)/libdozenosconfig$(EXTDLL) /usr/lib/$(LIBNAME)

clean:
	rm -rf $(BUILDDIR)
