mkdir logs

nice python3 train_logistic.py 1> logs/logistic.out 2> logs/logistic.err &
nice python3 train_svm.py 1> logs/svm.out 2> log/svm.err &
nice python3 train_nn.py 1> logs/nn.out 2> log/nn.err &
