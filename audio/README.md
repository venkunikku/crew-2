## Run Scripts in this Order:

1. Combines all noise files into one
```
merge-noise.py
```

2. Takes in the noise files and spits them out at the specified sample rate
```
downsample-noise.py
```

3. Cuts the merged noise file into n-second slices
```
slice-noise.py
```

4. Take in training files and spit them out in a single directory at the specified sample rate
```
downsample-training.py
```

5. Randomly mix noise samples with training samples
```
mix-noises-training.py
```

6. Prepare the data for further processing
```
label-matching.py
```


