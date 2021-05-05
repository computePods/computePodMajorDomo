# Dependency analysis

## Problem

While each ComputePod worker will have default knowledge of how to build 
objects in its area of specialty, this will often not be enough to build a 
large complex project which spans the domains of multiple workers. 

**How do we suplement the "default" dependency knowledge?**

### Examples

For example, ConTeXt document collections have a definite suggested 
structure using the [ConText Project 
structures](https://wiki.contextgarden.net/Project_structure).

Unfortunately, this "default" directory structure (and their associated 
ConTeXt declarations) does not include information about what diSimplex 
Code objects these ConTeXt documents might produce. The names of these 
code objects might have no relationship with, for example, the names of 
the containing ConTeXt documents. This means that, by default, the 
ComputePod workers will have no obvious way to infer that the request to 
build a given Code object, requires the typesetting of the associated 
ConTeXt documents. 

## Requirements

We need a simple text format in which to specify these *high-level* 
dependencies. This format also needs to be readable by multiple 
programming/scripting languages. This text format needs to support the 
specification of *"simple"* rules for associating artifacts with 
dependencies. 

Generally generic and/or details of dynamically generated dependencies 
*should* be located in the worker's associated ComputeChef plugins (and 
not the "high-level" project descriptions). 

## Solution

We will use a YAML format based upon the 
[Sake](https://github.com/tonyfischetti/sake) format to describe the 
dependencies in a *project*. This description should be sufficient to 
start the dependecy analysis phase. We expect the worker's ComputePodChefs 
to be able to fill in the fine dependency details as well as the rules 
required to build each (micro) step. The project description file will be 
located in the *top-level* of the project file directories. 

Project descriptions *will* *not* contain Python or Lua (or any Turing 
complete) code. They *may* contain wildcards describing other project 
files (which could be additional (sub)project description files).

### Potential formats

- **Our own format** This would require a parser etc... ;-(

- **YAML** This is a nice format which is easily human readable, and which 
  allows comments. There are Python, GoLang, and ANSI-C parsers, but 
  unfortunately there is no *pure* Lua *parser* (see 
  [lua-tinyyaml](https://github.com/peposso/lua-tinyyaml)). Generation of 
  these high-level project description files *should* be fairly easy in 
  most languages. 

  The use of (standard) "wildcard" characters ('*', '%', etc) in YAML 
  strings tends to confuse YAML parsers. Which means that users *must* put 
  "rules" inside quoted strings. 

- **JSON** This format is machine readable but can be rather wordy, and 
  does not allow comments. There are parsers in Python, GoLang, ANSI-C and 
  (pure) Lua (at least in ConTeXt's version). 

- **Lua** Pure Lua source code could be used as a text format. It can be 
  embedded in both ANSI-C, Python and GoLang. Unfortunately it is rather 
  *over* powered (being Turing Complete). 

- **Python** Pure Python source code could be used as a text format. It 
  could only be used in ANSI-C(?) and Python. Again, it is rather *over* 
  powered. 

## Questions

1. What sorts of dependency rules are used in build systems?

  - see: [Sake](http://tonyfischetti.github.io/sake/) for a YAML example

  - see: [tup](http://gittup.org/tup/) for an example of a simple 
    non-standard format. 

  - see: [Rake](https://ruby.github.io/rake/doc/rakefile_rdoc.html) for an 
    example of a Ruby DSL (which is ultimately Turing complete). 
  
2. How should we include more complex dependency rules? Sould/could we use 
   Python or Lua code? (Is this not too overpowered and a security risk?) 

   **A**: We will NOT include any Turing complete "code". Any such code 
   must be contained in the worker's Chef plugins (as python code), which 
   is "installed" at pod build time (rather than pod runtime).









