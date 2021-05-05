# User interface (webpages)

## Goal

We need a *simple* and *dynamic* user interface with which to control and 
monitor the ComputePods (ongoing) behaviour. This interface should be 
run-able inside modern browsers (such as FireFox and Chromium). 

## Nice to have

We will need a hierachical view of project files, as well as tasks and 
associated logfiles. 

Since the ComputePods will build up an intimate knowledge of the artifacts 
it builds, down to locations of cross-references, figures, chapters, 
sections, etc for ConTeXt, as well as varialbe and function definitions 
for ANSI-C and JoyLoL, it will eventually mmake sense to expose this 
knowledge by being able to "jump" to the textual source underlying each 
(generalized) reference. This suggests the use of an embedded "code" 
editor (CodeJar), as well as syntax highlighting (Prism).

The ability to have multiple panes open on tasks side by side, suggests 
the use of a split panel JavaScript tool (SplitJS).  

The ability to visualize the grapical networks of, for example, 
(potentially cyclic) build dependency networks, or concept cross-reference 
networks, suggests the use of D3 (and SVG). 

Word clouds, driven by D3, might make nice entries into the concept 
cross-reference networks (clouds). 

## Tools

Our objective in chosing tools is to keep things as "simple" and 
"independently" "mixable" as possible. At this point it is hard to see how 
we might want to mix and match tools to create a useful user experience. 

1. [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide)

  - [W3C DOM](https://www.w3.org/TR/DOM-Level-2-HTML/)

  - [Mozilla DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)

2. [Mithril](https://mithril.js.org/)

3. [Material Design Lite](https://getmdl.io/)

4. [D3](https://d3js.org/)

  - [D3-mitch-tree](https://github.com/deltoss/d3-mitch-tree)

5. [SplitJS](https://split.js.org/)

6. [CodeJar](https://medv.io/codejar/)

7. [Prism](https://prismjs.com/)
