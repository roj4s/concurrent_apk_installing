Python script to install an apk file into several devices concurrently.

It spawns several concurrent processes (By default equal to the numbers of cpus, or can passed in second parameter), executing an adb install command for each device.

Use: $ python script.py adress/of/apk [number_of_threads] 
