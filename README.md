# Getting Started

## Installation 

- Have aws account credentials defined under `~/.aws/credentials` (or make them somehow available to boto)
- Install the dependencies listed in `requirements.txt`
    - Ideally in a virtual environment i.e.
        ```
        virtualenv env 
        . env/bin/activate 
        pip install -r requirements.txt
        ```

## Usage

- To run the script with its default params:
```
./ec2_spot_instance_finder.py
```
    - If a virtualenv is used, activate it first i.e. `. env/bin/activate & ./ec2_spot_instance_finder.py`

## Example Response

The table bellow was generated using the default params and as such it is descendingly sorted by the `price_per_core` column.

```
   instance_type  cores    memory  memory_per_core  price_per_hour  price_per_core  price_per_gb  price_per_day  price_per_month
68      t1.micro      1     0.613         0.613000          0.0041        0.004100      0.006688         0.0984            2.952
35   i3.16xlarge     64   488.000         7.625000          0.5684        0.008881      0.001165        13.6416          409.248
39    i3.2xlarge      8    61.000         7.625000          0.0797        0.009962      0.001307         1.9128           57.384
19    i3.4xlarge     16   122.000         7.625000          0.1635        0.010219      0.001340         3.9240          117.720
5       i3.large      2    15.250         7.625000          0.0206        0.010300      0.001351         0.4944           14.832
6    r4.16xlarge     64   488.000         7.625000          0.6646        0.010384      0.001362        15.9504          478.512
2       r4.large      2    15.250         7.625000          0.0209        0.010450      0.001370         0.5016           15.048
53      m3.large      2     7.500         3.750000          0.0212        0.010600      0.002827         0.5088           15.264
43     i3.xlarge      4    30.500         7.625000          0.0445        0.011125      0.001459         1.0680           32.040
...
```

To sort by a different column e.g. by `memory_per_core`:
```
./ec2_spot_instance_finder.py --sort-by memory_per_core --desc
```


