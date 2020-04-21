nohup python3 -u train_hmm.py --trial_name $TRIAL_NAME \
	--local \
	--random_validation_set \
	--num_iterations 2 \
	--num_cep_coefs 13 \
	--multidimensional_input \
	--use_pomegranate \
	--distribution MultivariateGaussianDistribution \
	--n_threads 2 --training_prop 0.1 > training_logs_$TRIAL_NAME.txt 2>&1 &
