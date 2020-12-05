# BDTP
#### Big Data Transfer Protocol

This protocol sends big data on a address (IPv4,port)
compressing data with gzip module to make the transfer
even faster on slow networks and less data consumption.

Also this protocol prevents the `BrokenPipeError` while Sending data

## Sending/Receiving Data (client to host)

Here there are two scripts

1. host
2. client

where client is basically the script which is connecting to the host
and the host is the script which hosts the connection on itself.

Consider the following code as host script

```python
from denverapi import bdtp

address = ("localhost", 4000)  # they must be same in both script

data_receiver = bdtp.new_receive_data_host(address)
bdtp.launch(data_receiver)

data = data_receiver.data
```

and this as client script

```python
from denverapi import bdtp

address = ("localhost", 4000)
large_data = b"Some Large Data" * 100

data_sender = bdtp.new_send_data_port(large_data, address)
bdtp.launch(data_sender)
```

Breaking down the above code we have

---

```python
from denverapi import bdtp
```
First of all we import the library itself.

```python
address = ("localhost", 4000)
```
We specify the address where the socket connection is to happen

```python
large_data = b"Some Large Data" * 100  # Client Code
```
We prepare some data to send. You can change it to whatever you want but
it must be a python `bytes` object.

```python
data_sender = bdtp.new_send_data_port(large_data, address)  # Client Code
# -----------------------------------------------------------------------
data_receiver = bdtp.new_send_data_host(address)  # Sever Code
```
In the above code we initialize a sender and a receiver object.
***Note***: *Sender objects are required to be given data while all*
*other objects (including sender objects) require a pair of ipv4 and port address*

