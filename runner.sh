export PYTHONPATH=$PYTHONPATH:sentence-encoder

# run batch mode
#python main.py batch -input_file poc/answers.txt

# run inference mode
#python main.py inference -sentence "Το παράθυρο είναι ανοιχτό."


# run poc
python main.py batch -input_file poc/dataset.txt
python main.py poc -sentence "Θέλω να γίνω μέλος"