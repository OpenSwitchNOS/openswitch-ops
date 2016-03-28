# Pluggable Modules Test Cases

## Contents
- [Pluggable Modules DOM Information](#pluggable-modules-dom-information)

## Pluggable Modules DOM Information
### Objective
The test case verifies the DOM(Digital Optical Monitoring) information available on transceiver modules.

### Requirements
Physical switches are required for this test. The optical transceivers with DOM information are needed to verify the DOM parameters.

### Setup
#### Topology diagram

```ditaa
+----------+
|          |
|  Switch  |
|          |
+----------+
```

#### Test Setup
**Switch** with OpenSwitch and supported SFP+/QSFP+ transceiver modules plugged into repective ports.

### Description
1. Plug the DOM supporting SFP+/QSFP+ transceiver modules into the respective ports.
2. Verify whether the module is detected and supported by executing following command in **vtysh**.

    ***Switch Command***

    ```
    show interface 1 transceiver
    ```

    ***Switch Output***

    ```
	switch# show interface 1 transceiver
	Interface 1:
	 Connector: SFP+
	 Transceiver module: SFP_SR
	 Connector status: supported
	 ...
    ```

3. Verify the supported module's DOM information by executing following command in **vtysh**.

    ***Switch Command***

    ```
    show interface 1 dom
    ```

    ***Switch Output***

    ```
    switch# show interface 1 dom
	Interface 1:
	 Connector: SFP+
	 Transceiver module: SFP_SR
	  Temperature: 18.00C
      Temperature high alarm: Off
	  Temperature low alarm: Off
	  Temperature high warning: Off
	  Temperature low warning: Off
	  Temperature high alarm threshold: 73.00C
	  Temperature low alarm threshold: -3.00C
	  Temperature high warning threshold: 70.00C
	  Temperature low warning threshold: 0.00C
	  Voltage: 3.41V
	  Voltage high alarm: Off
	  Voltage high alarm: Off
	  Voltage high alarm: Off
	  Voltage low warning: Off
	  Voltage high alarm threshold: 3.80V
	  Voltage low alarm threshold: 2.81V
	  Voltage high warning threshold: 3.46V
	  Voltage low warning threshold: 3.13V
	  ...
    ```

4. Confirm the Voltage and Temperature value's from the module's DOM information to be in respective supported ranges.

    ***Error Message Output***
    ```
	Interface 50:
	 Connector: QSFP (splittable)
	 Transceiver module: QSFP_CR4
	 % No DOM information available
    ```

5. Verify the error message output if the module doesn't support DOM.

### Test result criteria
#### Test pass criteria
The test case is considered passing if either the DOM information like Temperature and Voltage in the module is in the proper supported range or by verifying the error message if the DOM information is not supported by the transceiver module.

#### Test fail criteria
The test case is considered failing in the following cases:

- The DOM information in the transceiver is out of range for Temperature or Voltage.
- If the error message validation fails for the modules not supporting DOM information.
