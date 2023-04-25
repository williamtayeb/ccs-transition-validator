```
ProcessList = S:1, S:2, S:3, S:4, S:5, S:6

SmUni = a.&b.P | SUM[list, i, P:i]
SmUni = a.&b.P | SUM[list, i, P:i]

SUM[i, I, S:i] ->(a) S:6


SmUni ::= (CM)[a/b,b/a]
SmUni ::= (CM)\{a,&b,c}

CM ::= a.&b.CM
CM:2 ::= c.&d.CM:2 + CM

CM:3 ::= ((CM) + (CM:2))
CM:4 ::= ((CM) | (CM:2))
```