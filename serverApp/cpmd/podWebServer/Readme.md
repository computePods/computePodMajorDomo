# Pod (only) WebServer

This pod (only) webserver is only accessible from *inside* a running 
computePod. 

It is *not* protected by https but it only listens on the localhost 
(127.0.0.1) interface. 

This allows this podWebServer to be accessible from simple processes such 
as, for example, a of ConTeXt module (using Lua).

Since the NATS server requires any client to authenticate itself using a 
TLS/SSL client certificate, this allows NATS messages to be sent from a 
simple process to NATS via the podWebServer. 
