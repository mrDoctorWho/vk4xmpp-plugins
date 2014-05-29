This module allow transport's admins to connect and administer transport itself via telnet connection.

**Requirements:**

*  telnetsrvlib — [github]( https://github.com/ianepperson/telnetsrvlib/ );

**Status**:

*  Alpha;

**Version**:

* 0.1a2;

**Compatibility**:

* vk4xmpp r156+;

**Authors**:

*  parts of code from telnetsrvlib example;

**Installation**:

1) Copy telnet.py into folder "extensions" in vk4xmpp root;

2) Move "telnetcfg_example.txt" to "telnetcfg.txt" and place it in vk4xmpp root;

3) Fill "telnetcfg.txt";

**Features**:

* Connection ip's white list (telnet);

* Config reload;

* Broadcast messages for transport's user;

* User list view;

* User deletion;

* Python code execution (one line);

**Known issues**:

* Sometimes initilization fails;

* Problems with eval/exec — one line support and syntax issues with symbols: '";

* Unicode problems on different systems.