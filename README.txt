Stable release of Data Cleaning tools 2019
Version 0
Diana Gooding: dgooding@bu.edu
2020 January 22

General data cleaning documentation: 
- DC document: sno+ document 5194-v1
- Water Unidoc
Presentation on this processing chain:
- sno+ document 6184-v1
__________________________________________
Sacrifice/

file: Data/n16_Nov2017.tar.gz
usage: tar -xzvf n16_Nov2017.tar.gz
output: Several directories with one n16 calibration ntuple each
function: Analysis scripts will run over each directory in parallel. Probably a smarter way to do this. 


file: scripts/rootreader.py
usage: must be in the same directory as the scripts that call it 
output: N/A
function: converts an ntuple into a python dictionary (Handy tool from Morgan Askins)


file: scripts/AllSac_chonk.py
usage: python AllSac_chonk.py /path/to/data/ out_name.root 
output: a root file for each ntuple containing two histograms of sacrifice for data cleaning cuts and classifier vs energy. 
function: After running over all data, you will have 104 root files. Hadd sum.root file1.root file2.root … to create sum.root, the total histograms for both DC and CC sacrifice that will be fitted in the next step. 


file: scripts/calc_sac.py
usage: python calc_sac.py
output: AvgSac.dat, containing the sacrifice for DC and CC. These numbers are the 1st  fit parameter of the flat-line fit. Input to contamination. 
function: fits a flat line in a hard coded energy range  to each histogram, and reports the 1st fit parameter as the sacrifices.  *** must put AvgSac.dat into Contamination/scripts in order for them to run ***


file: Batch/makebash_Sacrifice.py
usage: python makebash_Sacrifice.py
output: several job files and a job submission file that will submit the jobs with a delay, so as not to overwhelm the cluster
function: system for submitting analysis scripts in batch mode. You will need to edit the directories, run numbers, and delays in this script for your needs.  




Contamination/

file: Data/TB3_BlindedData_Subtuples_Teal.tar.gz
usage: tar -xzfv TB3_BlindedData_Subtuples_Teal.tar.gz
output: 9 directories with 1-2 subtuples from from Teal in each. These are blinded, subtupled (cut for noise, energy-corrected by Teal Pershing) ntuples from TB3. 
function: Analysis scripts will run over each directory in parallel. Because these are subtuples, the contamination scripts run in seconds. Full ntuples will take an hour or two, depending on your cluster’s resources and storage. 


file: scripts/Contamination_chonk2_blind.py
usage: python Contamination_chonk2_blind.py /path/to/data/ out_name evid_name
output: 
		- out_name, a text file with bifurcation box numbers listed
		- evid_name, a text file with bifurcation box event IDs listed
function: Fills bifurcation boxes for each ntuple. These out_name will be used in the final contamination step. 


file: scripts/snoleta.py
usage: python snoleta.py *note: AvgSac.dat from sacrifice step must be in the same directory as snoleta.py
output: prints contamination and Bifurcation box numbers to the terminal
function: loops over all out_name to fill total bifurcation boxes, and uses the sacrifice from AvgSac.dat to calculate contamination using the SNOLETA approach.


file: scripts/rootreader.py
usage: must be in the same directory as Contamination_chonk2_blind.py
output: N/A
function: converst ntuples into python dictionary (Handy tool from Morgan Askins)


file: Batch/makebash_Contamination.py
usage: python makebash_Contamination.py
output: several job files and a job submission file that will submit the jobs with a delay, so as not to overwhelm the cluster
function: system for submitting analysis scripts in batch mode. You will need to edit the directories, run numbers, and delays in this script for your needs.  




