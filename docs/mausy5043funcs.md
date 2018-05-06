## Usage ##
The following functions are provided:
***
### `fileops3` ###
This provides filesystem functions:  
* `contents` = cat(`filename`)
  returns the `contents` of the file `filename`.
* lock(`filename`)
  creates an empty file called `filename`.
* unlock(`filename`)
  removes the file `filename` (if it exists).
* syslog_trace(`message`, `priority`, `print_to_console`)
  send a (multi-line) message to syslog.
***
