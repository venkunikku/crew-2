nohup python3 -u train_hmm.py --trial_name 52G-RAM_20kHz_13CC_multi-dim_multi-state_200-iter_2-thread \
	--num_iterations 200 \
	--num_cep_coefs 13 \
	--multidimensional_input \
	--use_pomegranate \
	--distribution MultivariateGaussianDistribution \
	--n_threads 3 --training_prop 0.5 > training_logs.txt 2>&1 &
