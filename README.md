<p align="center">
  <h2 align="center">Morphing Network Slicing</h2>
  <p align="center">
  Alessandro Rizzetto [209783]
  </p>
</p>
<br>

## Table of contents
- [The project](#Intro)
- [Base topology](#Mininet)
- [How To](#Usage)
    - [Proof of Concept](#How_to_test)
        - [Linear topology](#Linear)
        - [Tree topology](#Tree)
        - [Star topology](#Star)

# Intro
The starting point of this project is a single domain base topology where we have full control of the network. The aim is to generate different slices as overlays of the original topology. This means that the actual base network remains unaltered but the perceived topology is different from the original one. It is important to understand that this is a virtualization process, new links can't be generated in the process of creating a new virtual slice.
This technique can be useful when a service provider wants to have different topologies on the same physical one.

# Mininet
We based our project on a partial mesh topology which gave us the flexibility needed to build multiple slices with different topologies on top of it.
The topologies that we have decided to implement are:
- Tree topology
- Linear topology
- Star topology

Specific base topology built with MININET: 
<p align="center">
  <img src="/pictures/BASE.png" width="700" height="420">
 
Table that maps each connection on the right port for every switch of the base topology:
|HOST|Port 1|Port 2|Port 3|Port 4|Port 5|Port 6|
|:--|:--:|:--:|:--:|:--:|:--:|:--:|
**S1**|  H1   | S2  | S3	| S4  | - | -
**S2**|  H2	  | S1	 | S4 | S5  | - | -
**S3**|  H3	  | S1	 | S4 | S6  | - | -
**S4**|  S1	  | S2	 | S3 | S5  | S6 | S7 
**S5**|  H4   | H5	 | S2 | S4  | S8 | -
**S6**|  H6	  | H7	 | S3 | S4  | S9 | -
**S7**|  S4	  | S8	 | S9 | S10 | - | -
**S8**|  H8   | S5   | S7 | S10 | - | -
**S9**|  H9	  | S6   | S7 | S10 | - | -
**S10**|  H10 | S8   | S9 | S7  | - | -

# Usage
```bash
git clone https://github.com/elrich2610/Morphing_Slices.git
cd Morphing_Slices
```
Two terminals are needed, one to run the ryu-controller and select the slice, the other to run the basic topology with Mininet.
If you installed Comnetsemu directly on your environment you can run everything from one terminal that will independently open the second one:
  
```bash
./start.py 
```
Otherwise, using Vagrant:

```bash
#Terminal 1
./start.sh [virtual topology name]
```
  
```
#Terminal 2
sudo python3 baseTopology.py
```
Now the chosen virtual slice has been created on top of the physical topology.

### How to test
Using the "pingall" Mininet command, it is feasible to verify the structure of the newly created virtual topology. This command allows you to check the connection beetween hosts and see that it indeed isn't the one of the base physical topology but the one determined by the running controller.
Otherwise is possible to use the script "dumpflow.sh" which dumps the flow for each switch.

### Linear:
With a view to creating a linear slice that connect S1,S2,S5,S8 only the path that connect these switch is preserved, cutting everything else.
The result show a linear slice connecting H1, H2, H5, H8 throung the S1,S2,S5,S8 channel.

<p align="center">
  <img src="/pictures/LINEAR.png" width="700" height="420">

### Tree:
With a view to creating a tree slice it is necessary to cut every connection involving S2, S3, s5, s6.
The resulting topology is a tree with root S1.
Even if we wanted to add more devices to the the base topology on the S1-S4-S7 path, the implemented tree-controller is still going to correctly generate a tree topology and the new links would all act accordingly.

<p align="center">
  <img src="/pictures/TREE.png" width="700" height="420">

### Star:
With a view to creating a star slice, only the paths that connects the center to the edge switches S1, S4, S5, S6, S7, S10 are preserved, any other connection is cut. The logic behind this slice is that any packet coming from a port that isn't part of the path that connects the device to the center is sent to the central switch of the virtual star topology otherwise the flooding algorithm is applied.
The resulting topology is a star where the packets must always go through the center to arrive at their destination.

<p align="center">
  <img src="/pictures/STAR.png" width="700" height="420">
