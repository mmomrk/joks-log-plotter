if (( $# >= 6 )); then
./plottr.py $* &&
echo command generated &&
chmod +x iplot.plt &&
./iplot.plt &&
feh -F plot.png;
else
./plottr.py -h;
fi
