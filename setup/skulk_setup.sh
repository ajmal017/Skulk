# Run command  bash skulk_setup.sh /Users/msivaanand/siva_projects/Skulk
echo $1
cd $1/setup/IB/
python3 setup.py install
cd $1/setup/
pip install -r requirement.txt