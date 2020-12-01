# denver
Denver API for Python

This API is specifically designed for python developers who want to use
advanced utilities but without coding much. The API requires you to
have minimum Python 3.8

## tools
this is a new package built into denver and now you can use every module inside it as a command line
tool. You can type the following command `python denverapi.tools` to get a list of available tools.

#### **WARNING**
The tools.cpic_editor is still a work in progress


## colored text (denver.ctext)
Colored console output have been a problem since long but here at denver API, we provide
cross-platform colored console output in almost any console. we also provide emulated
print and input function with extra keyword arguments for coloring and customizing. the
default print and input function of you code can be switched out to these one by
```python
from denverapi import ctext

print = ctext.print
input = ctext.input

# You can do the same with input
print("Hello", "World in colored", "text", fore="green", back="white", style="bright")
print("Hello", "World in simple", "environment")
```

## Installation
The package can be installed by
```commandline
pip install denver-api
```
and upgraded by
```commandline
pip install --upgrade denver-api
```

## Documentation
Documentation for denver can be found out at [this page](https://xcodz-dot.github.io/denverdocs) (*currently in progress
and may not be visible for some time*).
Also Documentation provided with this project can be used but you will have to install mkdocs
by the following command
```commandline
pip install mkdocs
```
or if you already have then you can upgrade it by following command
```commandline
pip install --upgrade mkdocs
```
After installation cd to `./docs/` and run this command `mkdocs build` or if you want to edit `mkdocs serve` and then 
you can edit any file (any file edited during `mkdocs serve` will be reflected on server every time you save a file)

## Community
This is a community driven project and accepts pull requests
of any kind (read [CONTRIBUTING.md](https://github.com/xcodz-dot/denver/blob/master/.github/CONTRIBUTING.md)), 
Thanks to all the contributors. Contributions are appreciated 

## Fixed Bugs
### 2.6.0b0
* `denverapi.tools.cpic_editor` cell height to width ratio is 25:10 now for better compatibility with terminal
### 2.5.2, 2.5.3, 2.5.4
* `denverapi.autopyb` fixes
### 2.5.1
* `denverapi.autopyb` minimum version fix
### 2.4.1
* `denverapi.bdtpfserv.post` function is now fixes to work without pausing and making troubles
* `denverapi.tools.bdtpserver` tool fixed for the post argument
* `denverapi.tools.cpic_editor` tool fixes which produced file system errors on linux
### 2.1.0
* `denverapi.pysetup.find_package_data` function is now fixed so it can include files at root level of a module

## What's New
### 2.6.0b0
* added new command line utilities.
* added `denverapi.tools.cpicview` to view cpic type images from commandline.
* added `entrypoints` to all tools as scripts.
* added `pyelib` which makes libraries from caching functions so they do not compile every time they run.
* added ability to `denverapi.autopyb.commands.pip` to be able to detect dependencies and do not run pip for no reason
* added ability to `denverapi.tools.cpic_editor` to save cpic images to file.
### 2.5.0
* autopyb is added as a new auto building manager
### 2.4.1
* Thread control
* Split up the pygame into a separate section (denverapi is sometimes required without pygame)
### 2.2.0
* new indev tools
* renamed to a new project
### 2.1.0
* `denver.tools` package is now added as a standard interface to many modules (Many tools are still work in progress)
