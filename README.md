# MDSCode
A compiler from simple code to mindustry code

## Disclaimer
This project is still in development and far from finished. So if you really need all the functionallity of mindustry this won't cut it yet.

## Getting started
The file extension of code files should be '.mdsc' (short for mindustry code)

Each line should end with a ; (Comming in languages as Java, JS, CSS, C, C# and the list goes on)

from // and further the line is a comment so everything after // to the end of the line is ignored

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

!! Warning. Please don't use variables starting with ``mdsc_`` those are reserved for the compiler.

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

### Native Mindsutry code
If you for some reason especially need to write in standard mindustry code you can by calling the ``exec`` function.
```
exec("set x 10"); // will set the variable x to the value 10
```