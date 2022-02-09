with open('venv2/test.py', 'w+') as f:
  f.write('import distutils.util')

from pylint.lint import Run

Run(["venv2/test.py", "--disable=all", "--enable=unused-import"])

import os
os.remove('venv2/test.py')
