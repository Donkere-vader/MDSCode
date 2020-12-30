# MDSCode
A compiler from simple code to mindustry code


## Examples

Printing to a messageblock:
```
%DEFINE msg_block = message1;

msg_block.print("test");
```

Writing to memory:
```
%DEFINE mem_block = cell1;

mem_block.write(100, 0):
```
Syntax:
```
<mememory_block>.write(<value>, <location>)
```