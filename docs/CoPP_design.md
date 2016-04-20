## Contents

  * [High-level design of control plane policing](#high-level-design-of-control-plane-policing)

# High-level design of control plane policing
Control plane policing (CoPP) protects usage of the CPU by prioritizing and rate-limiting control plane traffic. Currently implementation in OPS programs default classes with corresponding rate limit and queue values during plugin initialization. More detailed documentation of the design and defaults for opennsl based platforms can be found in the component design of opennsl plugin (/documents/dev/ops-switchd-opennsl-plugin/DESIGN).
