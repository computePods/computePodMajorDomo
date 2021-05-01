# ComputePods MajorDomo tool

## Architecture

MajorDomo is essentially a highly distributed build tool, which monitors 
its containers for changes and then can, depending upon what has changed 
and its current view of the build dependencies, will compute the minimal 
build possible. 

We use a system suggested by [tup](http://gittup.org/tup/) (see: [Build 
System Rules and Algorithms 
(PDF)](http://gittup.org/tup/build_system_rules_and_algorithms.pdf), 
see also [sake](https://github.com/tonyfischetti/sake)) 

We use [SyncThing's events 
pooling](https://docs.syncthing.net/rest/events-get.html#events-get) on 
the 
[LocalChangeDetected](https://docs.syncthing.net/events/localchangedetected.html) 
and 
[RemoteChangeDetected](https://docs.syncthing.net/events/remotechangedetected.html#remote-change-detected) 
events. This forms the basic "change set" between "updates".

## Resources

- [pynt](https://github.com/rags/pynt/) has an interesting use of Python 
  decorators. 
