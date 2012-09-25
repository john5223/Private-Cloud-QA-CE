Scripts
=====================
 
 This will be the scripts that Jenkins runs to test our enviroments

 Examples

 # Build Cloud Servers
python scripts/python/virtualized/environment/build_virt_env.py --username privateclouddevs --apikey 0e688a460988337e0e759524a2ccfc33 --number 5 --name "Alamo Virt Test" --project "Alamo Virt Testing" --os "Ubuntu 12.04 LTS (Precise Pangolin)" --flavor 512MB --dc dfw

# Gather Cloud Servers Info

python Documents/git/Private-Cloud-QA-CE/scripts/python/virtualized/environment/setup_virt_env.py --username privateclouddevs

# Setup Enviroment



# Tear Down Enviroment

python Documents/git/Private-Cloud-QA-CE/scripts/python/virtualized/environment/teardown_virt_env.py --username privateclouddevs --apikey 0e688a460988337e0e759524a2ccfc33 --name "Alamo Virt Test" --dc dfw