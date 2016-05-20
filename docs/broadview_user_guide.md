# BroadView Daemon
## Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [How to use feature](#how-to-use-feature)
  - [Configure basic configuration using CLI](#configure-basic-commands)
  - [Verify configuration using CLI](#verify-config)
 - [CLI](#cli)
 - [REST API](#rest-api)

## Overview
Networks have become business critical and Network Operators are demanding greater instrumentation and telemetry capabilities so that they can get better visibility into their networks. Increased visibility enables them to proactively identify problems that may lead to poor network performance. It also helps network operators to better plan and fine tune their networks to meet strict SLAs and improve and maintain Application performance. Broadcom has introduced   [BroadView](https://github.com/Broadcom-Switch/BroadView-Instrumentation) software suite -- an industry first -- that provides unprecedented visibility into switch silicon. BroadView exposes various instrumentation capabilities in Broadcom silicon and eases adoption of it by working with the ecosystem partners.

The suite consists of an Agent that runs on the switch and Application which interfaces with the Agent over Open REST API. Applications visualize, analyze data exported by the Agent, and provide the operator the ability to fine-tune the network. The Agent is Open and portable across different Network Operating Systems. The BroadView Daemon is the implementation of the Agent functionality in OpenSwitch.

The BroadView Daemon provides instrumentation capability for OpenSwitch. In the current release, it obtains MMU Buffer Statistics from Broadcom silicon and exports them via the REST API. This allows Apps to obtain the MMU Buffer stats and visualize buffer utilization patterns and detect microbursts. These help an operator to get visibility into the network and switch performance and fine tune the network. Some traffic, such as storage, requires lossless capability, and operators whose network carries these types of traffic are interested in learning about microbursts and tuning network to avoid packet drops during related congestion events.

The BroadView Daemon is recommended to be used with OpenSwitch running on a hardware platform (e.g. AS5712 from Accton).

## Prerequisites
Client Application which is needed to obtain MMU buffer statistics from BroadView Daemon must be downloaded and installed on a remote device.

## How to use the feature

BroadView Daemon runs as a background process in OpenSwitch.
The client application is used to fetch data from agent and display buffer statistics, it is also used to fine-tune various BST parameters.

### Configure basic configuration using CLI

 1. Configure agent port
 2. Configure remote client IP address and port number


### Verify configuration using CLI

 1. Verify configuration using BroadView CLI command (show broadview)
--------------
## CLI
CLI commands are described in a document named broadview_cli.

## REST API
Client Applications interface with the BroadView Daemon via [REST API](http://broadcom-switch.github.io/BroadView-Instrumentation/doc/html/dc/d3f/REST.html)

