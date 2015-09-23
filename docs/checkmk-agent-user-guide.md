
Openswitch Check_MK Agent User Guide
--------------------
The Openswitch Check_MK Agent is based on the [Check_MK Linux Agent] [1].  It is enabled by default in the Openswitch distribution and does not have any associated CLI commands (to enable/disable).

The Check_MK agent listens on TCP port 6556 for data collection queries. A quick way to test if the Check_MK agent is working as intended is by telnet-ing to the Openswitch node with port 6556:

    server> telnet openswitch 6556
    Trying 10.0.0.1...
	Connected to openswitch.
	Escape character is '^]'.
	<<<check_mk>>>
	Version: 1.1.8
	AgentOS: linux
	<<<df>>>
	/dev/sda1     ext3     1008888    223832    733808      24% /
		/dev/sdc1     ext3     1032088    284648    695012    30% /lib/modules
	<<<ps>>>
	init [3]
	/sbin/syslogd
	/sbin/klogd -x
	/usr/sbin/cron
	/sbin/getty 38400 tty2

For test purposes, the Check_MK agent can also be executed from the shell on an Openswitch node:

	openswitch> /usr/bin/checkmk-agent

This should output the same information as the telnet operation above.

###Configuration
Check_MK agent is invoked by systemd via socket activation. The Openswitch Chech_MK agent contains pre-configured standard systemd socket service activation files, `checkmk-agent@.service` and `checkmk-agent.socket`, which can be changed for site-specific customization of the Check_MK agent. Refer to [systemd.socket][2] for more information.


###Extending Check_MK Agent
The open source Linux Check_MK Agent is modified in Openswitch to report additional information specific to Openswitch. For example, interface statistics are fetched from OVSDB.

Check_MK reporting can be extended by adding check scripts in `/usr/lib/check_mk_agent/local`. Refer to [Check_MK documentation][3] for more details.
[1]: https://mathias-kettner.de/checkmk_linuxagent.html
[2]: http://www.freedesktop.org/software/systemd/man/systemd.socket.html
[3]: https://mathias-kettner.de/checkmk_localchecks.html
