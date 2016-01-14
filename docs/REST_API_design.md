High level design of REST API
============================

The feature is a combination of the REST API documentation rendering engine and the corresponding REST API service engine that serves the supported API functionalities.

Design choices
--------------
This feature sets and changes switch configurations as well as retrieves status and statistics information of the switch. It also serves as a building block for the web UI of the switch.

It mainly exposes operations on OVSDB through REST API. The resources serviced by the API is therefore based on the schema of the OVSDB.

Participating modules
---------------------
This feature has two modules:
- REST daemon (restd) -- Serving REST API requests.
- REST API rendering (restapi) -- Configured so that it points to the same host and the same port as the entry point for all the documented REST API operations.

```ditaa
           URL path
               +
               |
   +-----------+------------+
   +                        +
 /api                /rest/v1/system
   +                        +
   |                        |
   |                        |
   v                        v
REST API                REST API
rendering               servicing

```

The URL path name space is used to direct web requests to the appropriate module for processing accordingly to the diagram above.

During the switch image build time, the REST API servicing module generates and installs the REST API documentation file in JSON format for REST API rendering module to use at runtime.

OVSDB-Schema
------------
The new OVSDB schema is an extended schema file based on the original OVSDB schema file which is marked with two additional groups of tags to indicate how this feature should expose each resource through the REST API.

- The "category": ["configuration" | "status" | "statistics"] tags
indicate for each column of a table whether the attribute is a configuration (readable and writable), status (read-only) or statistics (mostly counters that change frequently). For those columns of the table that are not marked with any one of the category tags, they are not exposed in REST API.

- The "relationship": ["1:m" | "m:1" | "reference"] tags
indicate for those columns pointing to other tables whether the relationship between the table cited at the column and the current table is child ("1:m"), parent ("m:1") or reference. The REST API utilizes this information to construct resource structure among the tables in the schema file.

The two groups of tags can be used simultaneously when the column refers to some other table. For the columns that are tagged with "relationship", the "category" tag can be either "configuration" (read-write) or "status" (read-only).

A sanitizing Python script is run to strip the extended schema file of the two groups of tags added, so that other modules that is aware of the original OVSDB schema only can operate as usual.

HTTPS Support
-------------
REST API shall run only on https protocol. HTTPS protocol provides authentication of REST server and additionally provides encrytion of exhanged data between the REST server and client. Authentication/encryption is done by security protocols like SSL/TLS within HTTP connection.

REST server requires SSL certificate to run in HTTPS mode. Initially, REST server shall come up with a self-signed SSL certficate. The certificate and key files are located in "/etc/ssl/certs/ops.crt" and "/etc/ssl/certs/ops.key" respectively on the server. Steps to obtain a self-signed certficate is very much standard and is available on many websites. Self-signed SSL certificate is mainly for development purpose. For proper authentication, user may have to purchase a SSL certficate for a specific hostname from a trusted CA for e.g. symantec.

Once the SSL certificate is enrolled with a trusted CA, user shall copy the certificate file and private key file into predefined locations "/etc/ssl/certs/ops.crt" and "/etc/ssl/certs/ops.key" onto REST server using scp. To start sending requests to the REST server, the client side of the connection will have to use SSL context to point to the correct certificate file so that HTTPS connection can be established. Following is a sample client side code snippet that is compatible with python 2.7.9 to retrieve ports information from a REST server.
```ditaa
import ssl
import httplib

sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
sslcontext.verify_mode = ssl.CERT_REQUIRED
sslcontext.check_hostname = True
sslcontext.load_verify_locations("/etc/ssl/certs/ops.crt")
url = '/rest/v1/system/ports'
conn = httplib.HTTPSConnection("172.17.0.3", 443, context=sslcontext)
conn.request('GET', url, None, headers=_headers)
response = conn.getresponse()

```

Following is an example URL with https to query ports on the system from a web browser. HTTPS uses default port 443 if not specified.
```https://172.17.0.3/rest/v1/system/ports```


References
----------
* [REST API user guide](/documents/user/REST_API_user_guide)
* [REST API rendering component design](/documents/user/REST_API_design)
