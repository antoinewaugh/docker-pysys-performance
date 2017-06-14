# Results from pysys testing host v docker

We are seeing a significant overhead when running pysys' ProcessWrapper .startProcess() command from within Docker compared to a native linux host.

Considering the following pysys script

```
from pysys.constants import *
from pysys.basetest import BaseTest
from pysys.process.helper import ProcessWrapper

class PySysTest(BaseTest):
        def execute(self):
            process = ProcessWrapper('/usr/bin/echo', arguments=['sample line'],environs=os.environ,workingDir=os.getcwd(), state=FOREGROUND, timeout=None, stdout='/dev/null')
            process.start()

        def validate(self):
            self.assertTrue(True)
```

We find that run times on the host are approximately 0.05-0.1 seconds, and within a container anywhere from 1-10seconds.


## Host:

```
[antoine@localhost docker-pysys-performance]$ pysys run perf000.2

2017-06-14 14:48:22,692 INFO  ==============================================================
2017-06-14 14:48:22,693 INFO  Id   : perf000.2
2017-06-14 14:48:22,693 INFO  Title: Run system command using pysys ProcessWrapper.
2017-06-14 14:48:22,693 INFO  ==============================================================
2017-06-14 14:48:22,745 INFO  Assertion on boolean expression equal to true ... passed
2017-06-14 14:48:22,746 INFO  
2017-06-14 14:48:22,746 INFO  Test duration: 0.05 secs
2017-06-14 14:48:22,746 INFO  Test final outcome:  PASSED
2017-06-14 14:48:22,746 INFO  
2017-06-14 14:48:22,746 CRIT  
2017-06-14 14:48:22,746 CRIT  Test duration: 0.05 (secs)
2017-06-14 14:48:22,746 CRIT  
2017-06-14 14:48:22,746 CRIT  Summary of non passes: 
2017-06-14 14:48:22,746 CRIT  	THERE WERE NO NON PASSES
```

## Container:                                                       

```
[root@81895454240f perf]# pysys run perf000.2

2017-06-14 04:49:29,316 INFO  ==============================================================
2017-06-14 04:49:29,317 INFO  Id   : perf000.2
2017-06-14 04:49:29,317 INFO  Title: Run system command using pysys ProcessWrapper.
2017-06-14 04:49:29,317 INFO  ==============================================================
2017-06-14 04:49:30,220 INFO  Assertion on boolean expression equal to true ... passed
2017-06-14 04:49:30,220 INFO  
2017-06-14 04:49:30,220 INFO  Test duration: 0.90 secs
2017-06-14 04:49:30,220 INFO  Test final outcome:  PASSED
2017-06-14 04:49:30,220 INFO  
2017-06-14 04:49:30,221 CRIT  
2017-06-14 04:49:30,221 CRIT  Test duration: 0.91 (secs)
2017-06-14 04:49:30,221 CRIT  
2017-06-14 04:49:30,221 CRIT  Summary of non passes: 
2017-06-14 04:49:30,221 CRIT  	THERE WERE NO NON PASSES

```

# Profiling

In order to better understand which areas of code are taking the most time, the following commands were run on the host and within the container

```
python -m cProfile /apama_home/bin/pysys run perf000.2 > perf000.2.profile
```

The result indicates the majority of the delay/difference within wait & start

## Host
```
ncalls  tottime  percall  cumtime  percall filename:lineno(function)

1    	0.000    0.000    0.050    0.050 	commonwrapper.py:138(wait)
1   	0.000    0.000    0.051    0.051 	commonwrapper.py:160(start)

...

1    	0.050    0.050    0.050    0.050 	{time.sleep}

```

## Container
```

ncalls  tottime  percall  cumtime  percall filename:lineno(function)

 1    	0.000    0.000    1.002    1.002 	commonwrapper.py:138(wait)
 1    	0.000    0.000    1.002    1.002 	commonwrapper.py:160(start)
 
 ...
 
 20    	1.002    0.050    1.002    0.050 	{time.sleep}

```

After adding some additional logging within the `plat-unix/helper.py` , it appears the host calls os.waitpid() three times on average, whereas the docker container results in tens-hundreds of calls to os.waitpid().


## Long running containers: seeing this arbitrary 1 second difference drift to > 5 seconds per call to ProcessWrapper.start()

# Increased logging witin helper.py

## Host

```
antoine@localhost docker-pysys-performance]$ pysys run perf000.1

2017-06-14 16:23:47,731 INFO  ==============================================================
2017-06-14 16:23:47,732 INFO  Id   : perf000.1
2017-06-14 16:23:47,732 INFO  Title: Run system command using pysys ProcessWrapper.
2017-06-14 16:23:47,732 INFO  ==============================================================
2017-06-14 16:23:47,734 INFO  os.waitpid: 2017-06-14 16:23:47.734145
2017-06-14 16:23:47,734 INFO  os.waitpid: 2017-06-14 16:23:47.734557
2017-06-14 16:23:47,784 INFO  os.waitpid: 2017-06-14 16:23:47.784782
2017-06-14 16:23:47,785 INFO  Assertion on boolean expression equal to true ... passed
2017-06-14 16:23:47,785 INFO  
2017-06-14 16:23:47,785 INFO  Test duration: 0.05 secs
2017-06-14 16:23:47,785 INFO  Test final outcome:  PASSED
2017-06-14 16:23:47,785 INFO  
2017-06-14 16:23:47,785 CRIT  
2017-06-14 16:23:47,785 CRIT  Test duration: 0.05 (secs)
2017-06-14 16:23:47,786 CRIT  
2017-06-14 16:23:47,786 CRIT  Summary of non passes: 
2017-06-14 16:23:47,786 CRIT  	THERE WERE NO NON PASSES
```

## Container

```
2017-06-14 06:20:57,430 INFO  ==============================================================
2017-06-14 06:20:57,431 INFO  Id   : perf000.1
2017-06-14 06:20:57,431 INFO  Title: Run system command using pysys ProcessWrapper.
2017-06-14 06:20:57,431 INFO  ==============================================================
2017-06-14 06:20:57,432 INFO  os.waitpid: 2017-06-14 06:20:57.432458
2017-06-14 06:20:57,432 INFO  os.waitpid: 2017-06-14 06:20:57.432795
2017-06-14 06:20:57,483 INFO  os.waitpid: 2017-06-14 06:20:57.482986
2017-06-14 06:20:57,533 INFO  os.waitpid: 2017-06-14 06:20:57.533282
2017-06-14 06:20:57,583 INFO  os.waitpid: 2017-06-14 06:20:57.583605
2017-06-14 06:20:57,634 INFO  os.waitpid: 2017-06-14 06:20:57.633942
2017-06-14 06:20:57,684 INFO  os.waitpid: 2017-06-14 06:20:57.684257
2017-06-14 06:20:57,734 INFO  os.waitpid: 2017-06-14 06:20:57.734589
2017-06-14 06:20:57,784 INFO  os.waitpid: 2017-06-14 06:20:57.784906
2017-06-14 06:20:57,835 INFO  os.waitpid: 2017-06-14 06:20:57.835214
2017-06-14 06:20:57,885 INFO  os.waitpid: 2017-06-14 06:20:57.885519
2017-06-14 06:20:57,935 INFO  os.waitpid: 2017-06-14 06:20:57.935844
2017-06-14 06:20:57,986 INFO  os.waitpid: 2017-06-14 06:20:57.986180
2017-06-14 06:20:58,036 INFO  os.waitpid: 2017-06-14 06:20:58.036540
2017-06-14 06:20:58,086 INFO  os.waitpid: 2017-06-14 06:20:58.086880
2017-06-14 06:20:58,137 INFO  os.waitpid: 2017-06-14 06:20:58.137192
2017-06-14 06:20:58,187 INFO  os.waitpid: 2017-06-14 06:20:58.187519
2017-06-14 06:20:58,237 INFO  os.waitpid: 2017-06-14 06:20:58.237819
2017-06-14 06:20:58,288 INFO  os.waitpid: 2017-06-14 06:20:58.288161
2017-06-14 06:20:58,338 INFO  os.waitpid: 2017-06-14 06:20:58.338499
2017-06-14 06:20:58,388 INFO  os.waitpid: 2017-06-14 06:20:58.388904
2017-06-14 06:20:58,389 INFO  Assertion on boolean expression equal to true ... passed
2017-06-14 06:20:58,389 INFO  
2017-06-14 06:20:58,389 INFO  Test duration: 0.95 secs
2017-06-14 06:20:58,389 INFO  Test final outcome:  PASSED
2017-06-14 06:20:58,389 INFO  
2017-06-14 06:20:58,389 CRIT  
2017-06-14 06:20:58,389 CRIT  Test duration: 0.96 (secs)
2017-06-14 06:20:58,389 CRIT  
2017-06-14 06:20:58,389 CRIT  Summary of non passes: 
2017-06-14 06:20:58,389 CRIT  	THERE WERE NO NON PASSES
```
## Container after some time

```
[root@dd87d8391cc3 perf]# pysys run perf000.1
2017-06-14 06:34:30,114 INFO  ==============================================================
2017-06-14 06:34:30,116 INFO  Id   : perf000.1
2017-06-14 06:34:30,117 INFO  Title: Run system command using pysys ProcessWrapper.
2017-06-14 06:34:30,117 INFO  ==============================================================
2017-06-14 06:34:30,121 INFO  os.waitpid: 2017-06-14 06:34:30.121268
2017-06-14 06:34:30,122 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,123 INFO  os.waitpid: 2017-06-14 06:34:30.122928
2017-06-14 06:34:30,123 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,173 INFO  os.waitpid: 2017-06-14 06:34:30.173766
2017-06-14 06:34:30,174 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,225 INFO  os.waitpid: 2017-06-14 06:34:30.225004
2017-06-14 06:34:30,225 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,276 INFO  os.waitpid: 2017-06-14 06:34:30.276100
2017-06-14 06:34:30,276 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,327 INFO  os.waitpid: 2017-06-14 06:34:30.327232
2017-06-14 06:34:30,327 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,378 INFO  os.waitpid: 2017-06-14 06:34:30.378524
2017-06-14 06:34:30,379 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,429 INFO  os.waitpid: 2017-06-14 06:34:30.429708
2017-06-14 06:34:30,430 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,481 INFO  os.waitpid: 2017-06-14 06:34:30.480860
2017-06-14 06:34:30,481 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,532 INFO  os.waitpid: 2017-06-14 06:34:30.532017
2017-06-14 06:34:30,532 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,583 INFO  os.waitpid: 2017-06-14 06:34:30.583193
2017-06-14 06:34:30,583 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,634 INFO  os.waitpid: 2017-06-14 06:34:30.634419
2017-06-14 06:34:30,634 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,685 INFO  os.waitpid: 2017-06-14 06:34:30.685441
2017-06-14 06:34:30,686 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,736 INFO  os.waitpid: 2017-06-14 06:34:30.736586
2017-06-14 06:34:30,737 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,787 INFO  os.waitpid: 2017-06-14 06:34:30.787646
2017-06-14 06:34:30,788 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,839 INFO  os.waitpid: 2017-06-14 06:34:30.838963
2017-06-14 06:34:30,839 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,890 INFO  os.waitpid: 2017-06-14 06:34:30.890136
2017-06-14 06:34:30,890 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,941 INFO  os.waitpid: 2017-06-14 06:34:30.941282
2017-06-14 06:34:30,942 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:30,992 INFO  os.waitpid: 2017-06-14 06:34:30.992532
2017-06-14 06:34:30,993 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,043 INFO  os.waitpid: 2017-06-14 06:34:31.043583
2017-06-14 06:34:31,044 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,095 INFO  os.waitpid: 2017-06-14 06:34:31.094819
2017-06-14 06:34:31,095 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,146 INFO  os.waitpid: 2017-06-14 06:34:31.146534
2017-06-14 06:34:31,147 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,198 INFO  os.waitpid: 2017-06-14 06:34:31.198686
2017-06-14 06:34:31,199 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,250 INFO  os.waitpid: 2017-06-14 06:34:31.250212
2017-06-14 06:34:31,250 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,301 INFO  os.waitpid: 2017-06-14 06:34:31.301383
2017-06-14 06:34:31,302 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,352 INFO  os.waitpid: 2017-06-14 06:34:31.352535
2017-06-14 06:34:31,353 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,403 INFO  os.waitpid: 2017-06-14 06:34:31.403646
2017-06-14 06:34:31,404 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,454 INFO  os.waitpid: 2017-06-14 06:34:31.454792
2017-06-14 06:34:31,455 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,505 INFO  os.waitpid: 2017-06-14 06:34:31.505767
2017-06-14 06:34:31,506 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,557 INFO  os.waitpid: 2017-06-14 06:34:31.556992
2017-06-14 06:34:31,557 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,608 INFO  os.waitpid: 2017-06-14 06:34:31.608032
2017-06-14 06:34:31,608 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,659 INFO  os.waitpid: 2017-06-14 06:34:31.659300
2017-06-14 06:34:31,660 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,711 INFO  os.waitpid: 2017-06-14 06:34:31.710965
2017-06-14 06:34:31,711 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,762 INFO  os.waitpid: 2017-06-14 06:34:31.762127
2017-06-14 06:34:31,762 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,813 INFO  os.waitpid: 2017-06-14 06:34:31.813365
2017-06-14 06:34:31,814 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,864 INFO  os.waitpid: 2017-06-14 06:34:31.864611
2017-06-14 06:34:31,865 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,915 INFO  os.waitpid: 2017-06-14 06:34:31.915773
2017-06-14 06:34:31,916 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:31,967 INFO  os.waitpid: 2017-06-14 06:34:31.966838
2017-06-14 06:34:31,967 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,018 INFO  os.waitpid: 2017-06-14 06:34:32.018073
2017-06-14 06:34:32,018 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,069 INFO  os.waitpid: 2017-06-14 06:34:32.069163
2017-06-14 06:34:32,069 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,120 INFO  os.waitpid: 2017-06-14 06:34:32.120330
2017-06-14 06:34:32,120 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,171 INFO  os.waitpid: 2017-06-14 06:34:32.171494
2017-06-14 06:34:32,172 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,222 INFO  os.waitpid: 2017-06-14 06:34:32.222755
2017-06-14 06:34:32,223 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,274 INFO  os.waitpid: 2017-06-14 06:34:32.274211
2017-06-14 06:34:32,274 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,325 INFO  os.waitpid: 2017-06-14 06:34:32.325330
2017-06-14 06:34:32,325 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,376 INFO  os.waitpid: 2017-06-14 06:34:32.376479
2017-06-14 06:34:32,377 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,427 INFO  os.waitpid: 2017-06-14 06:34:32.427567
2017-06-14 06:34:32,428 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,479 INFO  os.waitpid: 2017-06-14 06:34:32.478998
2017-06-14 06:34:32,479 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,530 INFO  os.waitpid: 2017-06-14 06:34:32.530288
2017-06-14 06:34:32,530 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,581 INFO  os.waitpid: 2017-06-14 06:34:32.581411
2017-06-14 06:34:32,582 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,632 INFO  os.waitpid: 2017-06-14 06:34:32.632585
2017-06-14 06:34:32,633 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,684 INFO  os.waitpid: 2017-06-14 06:34:32.683711
2017-06-14 06:34:32,684 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,735 INFO  os.waitpid: 2017-06-14 06:34:32.734981
2017-06-14 06:34:32,735 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,786 INFO  os.waitpid: 2017-06-14 06:34:32.786232
2017-06-14 06:34:32,786 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,837 INFO  os.waitpid: 2017-06-14 06:34:32.837358
2017-06-14 06:34:32,838 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,888 INFO  os.waitpid: 2017-06-14 06:34:32.888775
2017-06-14 06:34:32,889 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,940 INFO  os.waitpid: 2017-06-14 06:34:32.940463
2017-06-14 06:34:32,941 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:32,991 INFO  os.waitpid: 2017-06-14 06:34:32.991711
2017-06-14 06:34:32,992 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,042 INFO  os.waitpid: 2017-06-14 06:34:33.042780
2017-06-14 06:34:33,043 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,094 INFO  os.waitpid: 2017-06-14 06:34:33.093893
2017-06-14 06:34:33,094 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,145 INFO  os.waitpid: 2017-06-14 06:34:33.145130
2017-06-14 06:34:33,145 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,196 INFO  os.waitpid: 2017-06-14 06:34:33.196363
2017-06-14 06:34:33,197 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,247 INFO  os.waitpid: 2017-06-14 06:34:33.247505
2017-06-14 06:34:33,248 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,298 INFO  os.waitpid: 2017-06-14 06:34:33.298534
2017-06-14 06:34:33,299 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,349 INFO  os.waitpid: 2017-06-14 06:34:33.349549
2017-06-14 06:34:33,350 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,400 INFO  os.waitpid: 2017-06-14 06:34:33.400604
2017-06-14 06:34:33,401 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,451 INFO  os.waitpid: 2017-06-14 06:34:33.451779
2017-06-14 06:34:33,452 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,502 INFO  os.waitpid: 2017-06-14 06:34:33.502799
2017-06-14 06:34:33,503 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,554 INFO  os.waitpid: 2017-06-14 06:34:33.554004
2017-06-14 06:34:33,554 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,605 INFO  os.waitpid: 2017-06-14 06:34:33.605112
2017-06-14 06:34:33,605 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,656 INFO  os.waitpid: 2017-06-14 06:34:33.656368
2017-06-14 06:34:33,656 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,707 INFO  os.waitpid: 2017-06-14 06:34:33.707514
2017-06-14 06:34:33,708 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,758 INFO  os.waitpid: 2017-06-14 06:34:33.758633
2017-06-14 06:34:33,759 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,809 INFO  os.waitpid: 2017-06-14 06:34:33.809772
2017-06-14 06:34:33,810 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,861 INFO  os.waitpid: 2017-06-14 06:34:33.860920
2017-06-14 06:34:33,861 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,912 INFO  os.waitpid: 2017-06-14 06:34:33.912021
2017-06-14 06:34:33,912 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:33,963 INFO  os.waitpid: 2017-06-14 06:34:33.963237
2017-06-14 06:34:33,963 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:34,014 INFO  os.waitpid: 2017-06-14 06:34:34.014382
2017-06-14 06:34:34,014 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:34,065 INFO  os.waitpid: 2017-06-14 06:34:34.065413
2017-06-14 06:34:34,066 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:34,117 INFO  os.waitpid: 2017-06-14 06:34:34.116838
2017-06-14 06:34:34,117 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:34,168 INFO  os.waitpid: 2017-06-14 06:34:34.167876
2017-06-14 06:34:34,168 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:34,219 INFO  os.waitpid: 2017-06-14 06:34:34.218933
2017-06-14 06:34:34,219 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:34,270 INFO  os.waitpid: 2017-06-14 06:34:34.270028
2017-06-14 06:34:34,270 INFO  pid: 0 /self.pid : 59
2017-06-14 06:34:34,321 INFO  os.waitpid: 2017-06-14 06:34:34.321245
2017-06-14 06:34:34,321 INFO  pid: 59 /self.pid : 59
2017-06-14 06:34:34,322 INFO  Assertion on boolean expression equal to true ... passed
2017-06-14 06:34:34,323 INFO  
2017-06-14 06:34:34,323 INFO  Test duration: 4.20 secs
2017-06-14 06:34:34,324 INFO  Test final outcome:  PASSED
2017-06-14 06:34:34,324 INFO  
2017-06-14 06:34:34,325 CRIT  
2017-06-14 06:34:34,325 CRIT  Test duration: 4.21 (secs)
2017-06-14 06:34:34,325 CRIT  
2017-06-14 06:34:34,325 CRIT  Summary of non passes: 
2017-06-14 06:34:34,325 CRIT  	THERE WERE NO NON PASSES

```

Questions:

* Do multiple (unsuccessful) calls to waitpid indicate child process has not yet started up? Or could it be that waitpid isnt responding but the process fork was fast?
