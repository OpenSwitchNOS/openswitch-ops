# High-level design of Access Control Lists (ACLs)
An Access Control List (ACL) is a list of Access Control Entries(ACEs),
ordered and prioritized by sequence numbers.  The entries are used to permit or
deny matching packets.  The current implementation supports IPv4 ACLs matching
on source IP address, destination IP address, IP protocol, source L4 ports and
destination L4 ports.  ACLs may be applied to L2 and L3 ports in the ingress
direction.

More detailed documentation of the design may be found in
ops-classifierd/src/acl/DESIGN.md.
