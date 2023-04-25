# Grammar

- EBNF
- `t` is a reserved action used for tau transitions

```
Definition = ( Constant | ProcessName ), 
  WhiteSpaceRequired, '::=', WhiteSpaceRequired, Expression ;

Expression = ProcessExpression, ModificationExpression ? ;

ProcessExpression = ( '(', ProcessExpressionElement, ')' ) |
  ProcessExpressionElement ;

ProcessExpressionElement = Constant | ProcessName |
  ActionPrefix | Sum | ParallelComposition ;

ModificationExpression = Relabelling | Restriction ;
ActionPrefix = Action, '.', Expression ;
Action = InputAction | OutputAction ;
InputAction = Label ;
OutputAction = '&', Label ;

Sum = Expression,
  WhiteSpaceRequired, '+', WhiteSpaceRequired, Expression ;

ParallelComposition = Expression,
  WhiteSpaceRequired, '|', WhiteSpaceRequired, Expression ;

Relabelling = '[' RelabellingList ']' ;
RelabellingList = Relabel, ( ',', WhiteSpace, Relabel ) * ;
Relabel = Label, '\', Label ;

Restriction = '\{' WhiteSpace, ActionList, WhiteSpace, '}' ;
ActionList = Action, ( ',', WhiteSpace, Action ) * ;

Transition = Expression,
  WhiteSpaceRequired, '->(', TransitionAction, ')',
  WhiteSpaceRequired, Expression ;

TransitionAction = Action | Tau ; 

```

# Tokens

```
// Tokens
Constant = "[A-Z][a-zA-Z]*" ;
ProcessName = Constant, "(:[0-9]+)?" ;
Label = "[a-z]*" ;
Tau = "t" // t is a reserved action which refers to tau
WhiteSpaceRequired = "[\s]+" ;
WhiteSpace = "[\s]*" ;
```