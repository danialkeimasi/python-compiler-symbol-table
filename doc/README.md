# Compiler Design Course: Tokenizer

you can read the [repo in github](https://github.com/danialkeimasi/python-regex-based-scanner).

### credits

Danial Keimasi

9612358036

# Grammar

```
program -> Statements
----
Statements -> Statement; Statements | Statement;
----
Statement -> IfStatement | ID(ParamList)
----
IfStatement -> if (Exp) { Statements } | if (Exp) { Statements } else { Statements }
----
Exp -> Param BIN_LOGIC_OP Param | Param
----
ParamList -> Param, ParamList | λ
----
Param -> CONST | ID
----
CONST -> CONSTSTR | CONSTNUM
```

# How to run the program

this is how you can compile your code using compiler_cli.py

```sh
python compiler_cli.py path/to/file
```

# input/output example

- We want to tokenize this file:

random_program/main.cpp

```cpp
some_var = "hello world" * 123;

if (some_var == 2) {
    print("it's equal");
}
```

- Using this command:

```sh

```
