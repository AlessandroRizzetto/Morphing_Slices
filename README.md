<p align="center">
  <h2 align="center">Morphing Network Slicing</h2>
  <p align="center">
  Alessandro Rizzetto
  </p>
</p>
<br>

## Table of contents
- [The project](#Intro)
- [Base topology](#Mininet)
- [How To](#Usage)
    - [Proof of Concept](#PoC)
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

# Usage

```bash
git clone https://github.com/elrich2610/Morphing_Slices.git
cd Morphing_Slices
```
From now on  **2** separate terminals are needed.
The first terminal is used to run the ryu-controller.
Each slice has its own ryu-controller, so it is necessary to run the one corresponding to the desired virtual topology.


```bash
#Terminal 1
./start.sh [virtual topology name]
```

On the  second terminal, run the physical base topology created with mininet; once started it'll automatically connect to the mininet console
```
#Terminal 2
sudo python3 baseTopology.py
```
Now the chosen virtual slice has been created on top of the physical topology.

### PoC
Using the "pingall" command, it is possible to verify the structure of the newly created virtual topology. This command allows you to follow the path of the packets and see that it indeed isn't the one of the base physical topology but the one determined by the running controller.
Another way to explore the newly created topology is to use the script "dumpflow.sh" which simply dumps the flow for each switch.

### Linear:
In order to create a slice with a linear topology only the path that connects S1, S2, and S3 is preserved, any other connection is cut.
The resulting topology connects H1, H2 and H4 through the S1-S2-S4 channel.

<p align="center">
  <img src="/pictures/LINEAR.png" width="700" height="420">

### Tree:
In order to create a slice with a tree topology it is necessary to cut every connection involving S2 or S3.
The resulting topology is an horizontal tree, oriented from left to right with root S1.
Even if we wanted to add more devices to the the base topology on the S1-S9-S10 path, the implemented tree-controller is still going to correctly generate a tree topology and the new links would all act accordingly.

<p align="center">
  <img src="/pictures/TREE.png" width="700" height="420">


### Star:
In order to create a slice with a star topology, only the paths that connects the center to the edge switches S1, S4, S5 and S6 are preserved, any other connection is cut. The logic behind this slice is that any packet coming from a port that isn't part of the path that connects the device to the center is sent to the central switch of the virtual star topology otherwise the flooding algorithm is applied.
The resulting topology is a star where the packets must always go through the center to arrive at their destination.

<p align="center">
  <img src="/pictures/STAR.png" width="700" height="420">
