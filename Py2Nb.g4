grammar Py2Nb ;

document  : block* ;
block     : CELLS stmts CELLE ;
stmts     : stmt* ;
stmt      : TEXT ;

CELLS   : '#' [ \t]* 'startcell' ;
CELLE   : '#' [ \t]* 'endcell' ;
TEXT    : ~[\r\n]+ ;
NEWLINE : [\r\n]+ -> skip ;
WS      : [ \t]+ -> skip;