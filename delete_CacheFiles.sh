#!/bin/bash

# Array mit Dateipfade
dateien=(
    "/home/sebi/filterRailTrackSwitches/dataset/railSem19/rs19_split8500/train/labels.cache"                 # rs19_split8500 train
    "/home/sebi/filterRailTrackSwitches/dataset/railSem19/rs19_split8500/test/labels.cache"                  # rs19_split8500 test
    "/home/sebi/filterRailTrackSwitches/dataset/railSem19/rs19_split8500/valid/labels.cache"                 # rs19_split8500 valid
    "/home/sebi/filterRailTrackSwitches/dataset/railSem19/rs19_split8500_onlySwitches/train/labels.cache"    # rs19_split8500_onlySwitches train
    "/home/sebi/filterRailTrackSwitches/dataset/railSem19/rs19_split8500_onlySwitches/test/labels.cache"     # rs19_split8500_onlySwitches test
    "/home/sebi/filterRailTrackSwitches/dataset/railSem19/rs19_split8500_onlySwitches/valid/labels.cache"    # rs19_split8500_onlySwitches valid
)

# überprüfe und lösche jede Datei
for datei in "${dateien[@]}"; do
    if [ -f "$datei" ]; then
        rm "$datei"
        echo "Die Datei '$datei' wurde gelöscht."
    else
        echo "Die Datei '$datei' existiert nicht."
    fi
done
