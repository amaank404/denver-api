# Contributing
Contributing to this repository is easy but must follow a few guidelines for perfect code submission. Also, we love
contributions from community.

## Code Format
Your code must comply with the requirements mentioned below.

### Must
* Your code must be PEP8 compliant (test will be conducted automatically when you submit a pull request)
* Your code must contain version, description, instructions in (classes, function, methods)
* Your code must be compatible with Python 3.6+

### Optional
* Your code should contain doctests (recommended)
* Your code should be optimized to work fast (recommended)

### Code Formatting Automation (black, isort automation)
You can completly forget about the code styling requirements and follow the following instructions to
automatically format it everytime.

#### Install The Denver Api in development mode
This process is only required once. (You might need to do it again every time you install denver-api from pip)

```bash
pip uninstall denver-api # Make sure you do not have any installed version
python setup.py develop
```

#### Format code using builtin automation script
The script named `make.py` contains code to fix things up just run the following commands every time
you encounter errors regarding code format

```bash
python make.py style
```

You can also run the below to check for errors

```bash
python make.py check
```

## Things You should know before you submit your code
* After submission of your code, your code will be open-source and will be distributed with MIT-License.
* You will not be able to delete it until your request is passed.
* You agree with all the above written statements.

## What's next?
After you are ready and you are willing to contribute just feel free to checkout the issues tab. There you
will finds label with community, those are the issues which are excepting community contribution. Also
you can add your own custom modules which function to provide user easy methods of hard tasks. The new modules
can be named and placed under `./denver/`.
