
echo "BUILD START"

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt


echo "BUILD END"