source ~/tensorflow/bin/activate
python preprocessing_main.py
deactivate

conda activate sbert
python3.6 sbert.py # Requires input
conda deactivate

source ~/tensorflow/bin/activate
python siamese.py
deactivate
