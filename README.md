# MicroPython Testing Framework

The framework uses an adapter interface to allow the test program to simulate
the effects of button presses and digital inputs on a system running MicroPython.

It also captures what is displayed and/or printed by the simulated system.

The system under test uses the Linux port of MicroPython, and the software under test needs to interact
with its host via an interface. The interface is actually an abstract base class.

It needs two implementations.

You use one when running your program on real hardware,
You use the other when testing your program.

The latter replaces real hardware interactions by interactions with the
test harness.

If your application runs on a single microcomputer you can run the test harness in a single proces.

If your application has multiple interacting microConrollers you can use Python's process
management tools to run multiple connected simulations. The simulations use zeromq
to interact with the test harness.

 



