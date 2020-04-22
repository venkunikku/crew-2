nohup python3 -u validate_hmm.py --trial_name $TRIAL_NAME \
        --local \
        --num_cep_coefs 13 > logs/validation_logs_$TRIAL_NAME.txt 2>&1 &
