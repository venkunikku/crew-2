## Run scripts in this order:

1. Combines all noise files into one
```
merge_noise.py
```

2. Takes in the noise files and spits them out at the specified sample rate
```
downsample_noise.py
```

3. Cuts the merged noise file into n-second slices
```
slice_noise.py
```

4. Take in training files and spit them out in a single directory at the specified sample rate
```
downsample_training.py
```

5. Randomly mix noise samples with training samples
```
mix_noises_training.py
```



