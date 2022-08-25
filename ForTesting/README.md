# TEST VERSION
This version of the project removes some of the basetopology outer ring links so that the creation of slices is more visible and better working.
Below are the outputs obtained by running the pingall command in mininet and the "dumpflow.sh" script (only some switch are shown).
<p align="center">
  <img src="/pictures/BaseV2.PNG" width="700" height="420">
  
## LINEAR SLICE
<p align="center">
  <img src="/pictures/LinearV2.PNG" width="700" height="420">
  
```bash
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 X X X X X X X
h2 -> h1 h3 X X X X X X X
h3 -> h1 h2 X X X X X X X
h4 -> X X X X X X X X X
h5 -> X X X X X X X X X
h6 -> X X X X X X X X X
h7 -> X X X X X X X X X
h8 -> X X X X X X X X X
h9 -> X X X X X X X X X
h10 -> X X X X X X X X X
*** Results: 57% dropped (6/90 received)
```

./dumpflow.sh:

```bash
            	===== S1 =====

in_port="s1-eth3",dl_dst=00:00:00:00:00:01 actions=output:"s1-eth1"
in_port="s1-eth1",dl_dst=00:00:00:00:00:02 actions=output:"s1-eth3"
in_port="s1-eth4",dl_dst=00:00:00:00:00:01 actions=output:"s1-eth1"
in_port="s1-eth1",dl_dst=00:00:00:00:00:03 actions=output:"s1-eth4"

            	===== S2 =====

in_port="s2-eth1",dl_dst=00:00:00:00:00:01 actions=output:"s2-eth3"
in_port="s2-eth3",dl_dst=00:00:00:00:00:02 actions=output:"s2-eth1"
in_port="s2-eth1",dl_dst=00:00:00:00:00:03 actions=output:"s2-eth3"
```
## STAR SLICE
<p align="center">
  <img src="/pictures/StarV2.PNG" width="700" height="420">

```bash
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 h6 h7 X X X
h2 -> h1 h3 h4 h5 h6 h7 X X X
h3 -> h1 h2 h4 h5 h6 h7 X X X
h4 -> h1 h2 h3 X h6 h7 X X X
h5 -> h1 h2 h3 X h6 h7 X X X
h6 -> h1 h2 h3 h4 h5 X X X X
h7 -> h1 h2 h3 h4 h5 X X X X
h8 -> X X X X X X X X X
h9 -> X X X X X X X X X
h10 -> X X X X X X X X X
*** Results: 57% dropped (38/90 received)
```
./dumpflow.sh:
```bash
             	===== S3 =====

in_port="s3-eth2",dl_dst=00:00:00:00:00:01 actions=output:"s3-eth1"
in_port="s3-eth2",dl_dst=00:00:00:00:00:02 actions=output:"s3-eth1"
in_port="s3-eth1",dl_dst=00:00:00:00:00:01 actions=output:"s3-eth2"
in_port="s3-eth2",dl_dst=00:00:00:00:00:03 actions=output:"s3-eth1"
in_port="s3-eth2",dl_dst=00:00:00:00:00:04 actions=output:"s3-eth1"
in_port="s3-eth2",dl_dst=00:00:00:00:00:05 actions=output:"s3-eth1"
in_port="s3-eth2",dl_dst=00:00:00:00:00:06 actions=output:"s3-eth1"
in_port="s3-eth2",dl_dst=00:00:00:00:00:07 actions=output:"s3-eth1"
in_port="s3-eth1",dl_dst=00:00:00:00:00:02 actions=output:"s3-eth2"
in_port="s3-eth1",dl_dst=00:00:00:00:00:04 actions=output:"s3-eth2"
in_port="s3-eth1",dl_dst=00:00:00:00:00:05 actions=output:"s3-eth2"
in_port="s3-eth1",dl_dst=00:00:00:00:00:06 actions=output:"s3-eth2"
in_port="s3-eth1",dl_dst=00:00:00:00:00:07 actions=output:"s3-eth2"

            	===== S4 =====

 cookie=0x0, duration=204.303s, table=0, n_packets=400, n_bytes=26084, priority=0 actions=CONTROLLER:65535
```
## TREE SLICE
<p align="center">
  <img src="/pictures/TreeV2.PNG" width="700" height="420">
  
```bash
mininet> pingall
*** Ping: testing ping reachability
h1 -> X X X X X X h8 h9 h10
h2 -> X X X X X X X X X
h3 -> X X X X X X X X X
h4 -> X X X X X X X X X
h5 -> X X X X X X X X X
h6 -> X X X X X X X X X
h7 -> X X X X X X X X X
h8 -> h1 X X X X X X h9 h10
h9 -> h1 X X X X X X h8 h10
h10 -> h1 X X X X X X h8 h9
*** Results: 86% dropped (12/90 received)
```
./dumpflow.sh:
```bash
            	===== S1 =====

in_port="s1-eth2",dl_dst=00:00:00:00:00:01 actions=output:"s1-eth1"
in_port="s1-eth1",dl_dst=00:00:00:00:00:08 actions=output:"s1-eth2"
in_port="s1-eth1",dl_dst=00:00:00:00:00:09 actions=output:"s1-eth2"

```



