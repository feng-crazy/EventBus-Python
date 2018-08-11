# EventBus-Python
A synchronous event framework，Use ZMQ's XSUB/XPUB
This project is an application framework for event synchronization.
Focus on uncoupling the code and make it easy to extend the program.
This code supports multiple threads and processes.
Use ZMQ's XSUB/XPUB as an event bus,Each of the classes that inherit from EventTarget can publish and subscribe to events.
The publisher sends the event to the bus, which then informs all subscribers to process the event
