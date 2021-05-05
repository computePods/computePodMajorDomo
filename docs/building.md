# Building an object

## Problem

How does a user specify something to be built?

We would *like* to simply specify the resulting object and the ComputePod 
system will then determine what needs to be built. 

There are a number of phases in building an object:

1. Dependency Analysis (building an internal dependency graph (which 
because of ConTeXt *is* *cyclic*)).

2. Execution of the build 

  - we plan to use a [tup](http://gittup.org/tup/) style build execution. 
    (see: [Build System Rules and Algorithms 
    (PDF)](http://gittup.org/tup/build_system_rules_and_algorithms.pdf), see 
    also [sake](https://github.com/tonyfischetti/sake))) 

## Solution

To specify something to be built, the user will specify a high-level 
(YAML) project description file as well as a "target" described in the 
description file. 

These project description files arelocated in the top-level of the project 
directory hierarchy. 

A user specifies three things:

1. A project (a directory inside the user's ComputePod assigned area)

2. A project description file (inside the top-level directory of the 
   project).

3. A project target (specified inside the project description).

## Questions

1. How does the system know which workers can add to the dependency 
   analysis: 

     - if there are multiple (possible) ways to build the same object? 

     - if there are no "bridges" between types of artifacts (such as the 
       ConTeXt documents which "create" source code)? 
       
   **A**: All of this high-level detail *should* be specified in the 
   project description file. 
