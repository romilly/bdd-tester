# TO DO


1. Button presses
    1. Button should go down for a configurable period
    1. Relevant pin should also go high
    
1. Pins
    1. Can set pins high or low from controller
    1. Can read pin state
    
1. Refactoring
    1. ~~Tidy up listener, publisher, runner from MicrobitController~~
    1. Do I need separate channels (one per 'bit) for event notification?
    1. ~~Use ChainOfResponsibility for commands~~

1. micro:bits can send radio messages
    1. send using pub-sub with multiple senders, receivers
    1. use channel, address, group
    1. check senders don't see their own messages

## Radio

Once the controller has started each micro:bit and each has checked in,
each micro:bit in turn needs to connect to every other microbit's radio channel.
and send another checkin message to the controller.
    
    
    


