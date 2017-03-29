Wrapper for Linux native “rsync” utility, that provides an easy way to replicate files from local to remote host.

The requirements are the following:

The Python script should be a single file, but in the future we want to scale it into a Python package (multiple files for each functionality) – please mind that
Should be reusable. It should contain an interface (function or functions) which will allow to use it in another scripts.
Should support a CLI - could be launched from bash with arguments and keys.
Should support keys from rsync: -PavSzq, -progress, '-e ssh -P -i'
Should support password from CLI option (if provided): syncer.py –pass='No1LiveS4ever' file1.txt root:22@hostname:/
Valid separators between username and port are: comma, spot, colon (,.:)
Should check if path exists on remote host and if not then create it.
