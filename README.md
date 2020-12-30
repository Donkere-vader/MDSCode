# MDSCode
A compiler from simple code to mindustry code


## Getting started
The file extension of code files should be '.mdsc' (short for mindustry code)

### Defining
At the top of your script define all the blocks for easy acces and changing in the future:
```
%DEFINE msg_block = message1;
%DEFINE memory = cell1;
%DEFINE core = nucleus1;
```

### Variables
Variable setting is very straight forward.
```
var = 1;
one_plus_two = 1 + 2;
```

### Print
Printing is a function of the "class" msg_block.
```
msg_block.print("print_value");
// prints (and flushes) the value to message1
```

### Memory
Writing and reading is also a function of a memory "class".

#### Write
```
memory.write(100, 0); // write the value 100 to location 0
```
#### Read
```
memory.read(0); // read the value at position 0
```

### Sensor
You can get information of any block as if it is a variable of the class.
```
amount_of_copper_in_nucleus = core.copper;
nucleus_item_cap = core.itemCapacity;
```

### Defining custom functions
Comming soon

### If statements
Comming soon