files=`ls *txt -1`
#files=test.txt
for fil in $files; do
	echo $fil
	sed -i.bak -r 's/,/\./g' $fil
done;

