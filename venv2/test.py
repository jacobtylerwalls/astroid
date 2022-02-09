with open('venv2/a.py', 'w+') as f:
  f.write('import distutils.util')

from pylint.lint import Run

Run(["venv2/a.py", "--disable=all", "--enable=unused-import"])

import os
os.remove('venv2/a.py')
