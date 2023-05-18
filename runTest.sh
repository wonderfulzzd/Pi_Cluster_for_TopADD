#!/usr/bin/env bash

# Define a timestamp function
timestamp() {
  date +"%Y-%m-%d_%H-%M-%S"
}

rm terminal_output* time_recording*

mesh=64
for dim in 2 3; do

  if [ dim == 2 ]; then
    mesh=240
    sed -i -e "s:rawP += fin\.read(8\*8\*nCellsT\[i\]):rawP += fin\.read(4\*8\*nCellsT\[i\]):g" ./bin2vtu.py
  elif [ dim == 3 ]; then
    mesh=64
    sed -i -e "s:rawP += fin\.read(4\*8\*nCellsT\[i\]):rawP += fin\.read(8\*8\*nCellsT\[i\]):g" ./bin2vtu.py
  fi

  sed -i "/#define DIM/c\#define DIM $dim                 // 2-2D, 3-3D" ./options.h

  make myclean; make -j4 topopt;

  for np in 16 12 8 4 1; do
    dateTime=`date +"%Y-%m-%d_%H-%M-%S"`
    outputFileName="terminal_output_${dateTime}_${dim}_${mesh}_${np}.txt"
    timeFileName="time_recording_${dateTime}_${dim}_${mesh}_${np}.txt"

    timestamp 2>&1 | tee $outputFileName

    SECONDS=0
    (mpirun -n $np -hostfile machinefile ./topopt) 2>&1 | tee -a $outputFileName
    duration=$SECONDS

    timestamp 2>&1 | tee -a $outputFileName

    (echo "Time elapsed using $np processes: $duration s") 2>&1 | tee -a $outputFileName
    (echo "Time elapsed using $np processes: $duration s") 2>&1 | tee -a $timeFileName
    done
done

sed -i "/#define DIM/c\#define DIM 2                 // 2-2D, 3-3D" ./options.h
sed -i -e "s:rawP += fin\.read(8\*8\*nCellsT\[i\]):rawP += fin\.read(4\*8\*nCellsT\[i\]):g" ./bin2vtu.py
