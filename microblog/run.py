"""
The shebang line in any script determines the script's ability to be executed like an standalone executable without
typing python beforehand in the terminal or when double clicking it in a file manager(when configured properly). It
isn't necessary but generally put there so when someone sees the file opened in an editor, they immediately know what
they're looking at. However, which shebang line you use IS important; Correct usage is:

#!/usr/bin/env python
#!/usr/bin/env python Usually defaults to python 2.7.latest, and the following defaults to 3.latest

#!/usr/bin/env python3
DO NOT Use:

#!/usr/local/bin/python
"python may be installed at /usr/bin/python or /bin/python in those cases, the above #! will fail."
"""

#!venv/bin/python
from microblog.app import app
app.run(debug=True)