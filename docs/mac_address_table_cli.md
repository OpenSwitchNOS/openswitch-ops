# Display Support for mac address table

## Contents

- [Display commands](#display-commands)

## Display commands

### show mac-address-table

#### Syntax

```
show mac-address-table [dynamic | static | hw-vtep] [port <ports> | vlan <VLAN_ID>]  [tunnel <tunnel-key>] [address  <A:B:C:D:E:F>]
```

#### Description

This command displays all the learned or static MAC address in the device with following information.

-	MAC address
-	VLAN Information
-	Self learned from ASIC or statically configured
-	Port name

#### Authority

Admin User.

#### Parameters

N/A

#### Examples

```
switch# show mac-address-table
MAC age-time            : 300 seconds
Number of MAC addresses : 3

MAC Address          VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:01   1        static     1
00:01:01:01:01:02   2        learning   2
00:01:01:01:01:03   1        learning   3
switch#

```

### show mac-address-table [ dynamic | static ]

#### Syntax

```
 show mac-address-table [ dynamic | static ] [ port < 2 | 1-2 > ]
```

#### Description

This command displays details of all the learned or static MAC address on the specified ports.

#### Authority

Admin User.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| ** 1 or 1-2 or 1,lag1 ** | Optional | 1-2,3 | Shows all the learned or static MAC address on these ports.|

#### Examples

```
switch# show mac-address-table dynamic port 1
MAC age-time            : 300 seconds
Number of MAC addresses : 1

MAC Address          VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:03    1        learning    1

switch# show mac-address-table dynamic port 1-2
MAC age-time            : 300 seconds
Number of MAC addresses : 2

MAC Address          VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:02    2        learning   2
00:01:01:01:01:03    1        learning   1

switch# show mac-address-table static port 1
MAC age-time            : 300 seconds
Number of MAC addresses : 1

MAC Address          VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:03    1        static    1
```

#### Syntax

```
 show mac-address-table [ dynamic | static ] [ vlan < 2 | 1-2 > ]
```

#### Description

This command displays details of all the learned or static MAC address on the specified VLANS.

#### Authority

Admin User.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| ** 1 or 1-2 ** | Optional | 1-2,3 | Shows all the learned or static MAC address on these VLANS.|

#### Examples

```
switch# show mac-address-table dynamic vlan 1
MAC age-time            : 300 seconds
Number of MAC addresses : 1

MAC Address        VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:03   1       learning    1

switch# show mac-address-table dynamic vlan 2-3
MAC age-time            : 300 seconds
Number of MAC addresses : 2

MAC Address          VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:02     2        learning   2
00:01:01:01:0c:02     3        learning   2

switch# show mac-address-table static vlan 1
MAC age-time            : 300 seconds
Number of MAC addresses : 1

MAC Address        VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:03   1       static    1
```

### show mac-address-table tunnel < tunnel-key >

#### Syntax

```
 show mac-address-table tunnel < 7 >
```

#### Description

This command displays all the MAC address learned on this tunnel interface.

#### Authority

Admin User.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **< tunnel-key >** | Required | < 7 > | Shows all the MAC learned on this tunnel port.|

#### Examples

```
switch# show mac-address-table tunnel 7
MAC age-time            : 300 seconds
Number of MAC addresses : 1

MAC Address          VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:03     1       learning     1

```

### show mac-address-table address < mac-address >

#### Syntax

```
 show mac-address-table address <A:B:C:D:E:F>
```

#### Description

This command displays details of specific MAC address learned  by the device.

#### Authority

Admin User.

#### Parameters

| Parameter | Status   | Syntax | Description |
|-----------|----------|----------------------|
| **< A:B:C:D:E:F >** | Required | < A:B:C:D:E:F > | Shows details of the specific MAC address.|

#### Examples

```
switch# show mac-address-table address 00:01:01:01:01:03
MAC age-time            : 300 seconds
Number of MAC addresses : 1

MAC Address          VLAN     Type      Port
--------------------------------------------------
00:01:01:01:01:03   1        learning     1
```
