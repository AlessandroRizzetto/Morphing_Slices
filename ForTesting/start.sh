#/usr/bin/bash
topo=(star star2 tree linear ring);

if [[ " "${topo[@]}" " == *" "$1" "* ]]
then
		val=$1
else
		echo ""
		echo "Invalid topology."
		echo "['star', 'star2','ring', 'tree', 'linear']"
		echo ""
		exit 1
fi
echo ""
echo "Starting the controller with a <${val}> topology."
echo ""
sudo fuser -k 6653/tcp
ryu-manager ./topology/${val}.py
