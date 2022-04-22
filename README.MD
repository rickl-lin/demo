# Doxygen

Doxygen is a program file generation tool, which can convert specific annotations in the program into description files, and organize the annotations into a reference manual after processing.
Doxygen can also understand the relationship between elements by including dependency graphs and inheritance graphs.


### Environment:
Linux
### Installation:
* Install the program in the linux terminal.

`sudo apt-get install doxygen`

* Drawing relational graph through graphviz.
`sudo apt-get install graphviz`

### Usage:
* The generated profile Doxyfile in the directory where you want to execute doxygen. You can edit the configuration file to let it matches your project. Skip this step if you already have a Doxyfile. You just need to move the Doxyfile to the directory where you want to execute doxygen.
`doxygen -g`

* Doxygen generate the documentation, based on your settings in the configuration file.
`doxygen Doxyfile`

* The generated html documentation will be stored in docs. You can open the html file and search for "index.html" then you can see the description file.
