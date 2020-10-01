# Brief
This page contains information about every module in the project.

## [bcli](modules/bcli.md)
This module is usually useful for beautiful command line interface
for users. the user can easily understand with the help of cross-platform
coloring solutions which is a good sign and what is the bad sign, Nothing.

bcli's default format contains the following functions.

* good (green color)
* bad (red color)
* info (yellow color)
* run (bright white color)
* input (emulates default input function with blue colored input prompt)

all the above function emulates complete print function except for input
which emulates input function.

## [bdtp](modules/bdtp.md)
This module is all about sockets, many times it happens that you are unable
to send up large data with sockets and you are not willing to write
tons of lines for the same. So here we are, we implement the easiest methods
for implementing sockets for big data transfer. we provide

* Host side sending
* Client side sending
* Host side receiving
* Client side receiving

Also there are situations where you have a socket already hosted but want
to implement our API. No Problems, we provide the following features.

* Use BDTP with existing socket
* Get the average speed of the socket
* Compress data to save data over internet, also resulting in fast transfer on slow
  connections

## [bdtpfserv](modules/bdtpfserv.md)
We have solved the problem of data transfer using BDTP but now the
problem is with hosting files on the server. Well, that requires a lot of lines
for hosting and getting the things but why to worry we provide the module for that.
It basically provide the following features for you to work with

* Hosting solution for hosting your files which are within a directory. Also, you can
  simply specify the sub directory of the files hosting service to limit user posts to
  that directory.
* Function like listdir, mkdir, post, get to retrieve files and data
* Our hosting service is also supports multi-threaded get functionality.

## [bitmap](modules/bitmap.md)

BitMap module is a little weird because you can not save images or load images, but
instead you can work on Ascii images using it. Ok, I know that is not something
you might have thought because that can be done with the inbuilt list. But check
out the features below

* bitmap allows you to write images without any index errors also just by 
  `image[x, y]` syntax. Also, it will just ignore anything that is set outside the
  bitmap.
* bitmap portions allows you to get a reference to a part of image, basically
  if you edit something in bitmap portion, they will be directly reflected over bitmap.
  Also, your image would not be overwritten after a certain limit of height and width.
  
## [crypt](modules/crypt.md)

It is very sure that you might have encountered security issues with your program and
you might look for a very simple library to do your task, so here we are we bring
you the crypt which features

* morse code
* basic encode
* reverse cipher
* caesar cipher
* transposition cipher
* affine cipher
* substitution cipher
* vigenere cipher

also you can simply use the new feature cipher combinator for making a class which can
encrypt your code with multiple ciphers.

## [ctext](modules/ctext.md)
ctext is are favorite and best module we have ever built, because it is cross platform console
coloring system which supports colors for both windows and unix based os. Also this module is
loaded with tons of features like emulated print and input function which you can easily use
in place of builtin print and input functions they are very simple to apply. You can also use
other features

* terminal size query
* clear line
* clear screen
* style text
* code to character
* window title set
* cursor movement in all direction
* print at position
* formatted escape sequence

## [datau](modules/datau.md)
Data Unicode might not be good enough to satisfy your needs but we have a prebuild library of
replacement dictionaries which are escaped by function `convert`, it converts multiline text into
the useful unicode text using the dictionaries for example you can convert the following

    /-------\
    | Hello |
    \-------/

into a very nice unicode text which does not show ugly looking spaced between them

You can probably try this example to know about an example
```python
from denver import datau

my_box = """
/-------\\
| Hello |
\\-------/
""" # you might need to escape back slashes, we recommend using files for storing and retrieving data

my_smooth_box = datau.convert(my_box, datau.box['soft box'])
print(my_smooth_box)
```

## [datp](modules/datp.md)
This class is awesome for list representation also datp means Data Processor.
we provide some of the good methods like List printing using indentation or tree2 for other type of list representation
and tree3 for representation of dictionaries. we also privide StorageTree to extract files
under a folder into VSD (Virtual Storage Dictionary).

## [get](modules/get.md)
this module is just awesome for anyone not gud at taking input from user or may be validating it, you can use its
print tree method to print directories or you can simply use get file path to get a
path to file from user input. there are tons of features

* tree printer
* screen clear
* path input
* ipv4 validator
* (ipv4, port) input

## [graphics3d](modules/graphics3d.md)
Well this module is loaded with a few algorithms and a fully featured model viewer by which you can view models very
easily. There are many algorithms that

* flattens a 3d vector point to 2d rendered vector point
* rotate a 3d vector point around its axis
* model flatten
* model rotate
* model maker
* model dump to file
* model load from file
* model viewer

## [handypy](modules/handypy.md)
This module have functionalities for interacting with real python 3 code. it contains the following
featurs

* analise of imports made by source file

that's all for this small module

## [log](modules/log.md)
This module provides you with basic logging facilities which
can be used by your programs to get developed easily. while
debugging you can keep the configurations on and while
releasing you can switch of error, warnings, debug or you
can also change the file to a new file which can contain
the log.

