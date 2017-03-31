Wrapper for Linux native “rsync” utility, that provides an easy way to replicate files from local to remote host.

The requirements are the following:

The Python script should be a single file, but in the future we want to scale it into a Python package (multiple files for each functionality) – please mind that
Should be reusable. It should contain an interface (function or functions) which will allow to use it in another scripts.
Should support a CLI - could be launched from bash with arguments and keys.
Should support keys from rsync: -PavSzq, -progress, '-e ssh -P -i'
Should support password from CLI option (if provided): syncer.py –pass='No1LiveS4ever' file1.txt root:22@hostname:/
Valid separators between username and port are: comma, spot, colon (,.:)
Should check if path exists on remote host and if not then create it.

Usage.
How the one can use this script. It has pretty much the same usage as nomral 'rsync' cmd with few exeptions,
examples:
like that '(.,):80' u will be able to choose port 80 for ssh connection,
  -  python rsyncer.py /dir file1.txt username:80@remotehost:/dir
or u can use 'rsync' to transer data to a miltiple remote hosts like this,
  -  python rsyncer.py /dir file1.txt [ username1:80@remotehost1:/dir1 username2@remotehost2:/dir2 ]
Remember, if you are going to use the last case, u have to separate perentheses with spaces (' [ ' and ' ] '), or u will get an error otherwise.

We are currently working on interactive console 'help' to make our application more userfirendly.
