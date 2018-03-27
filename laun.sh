if (( $# >= 6 )); then
./plottr.py $*
./iplot.plt
feh -F plot.png;
else
./plottr.py -h;
fi
