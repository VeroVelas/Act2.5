
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ERROR IDENTIFIER KEYWORD NUMBER SYMBOLprogram : class_declarationclass_declaration : KEYWORD IDENTIFIER SYMBOL SYMBOL method_declaration SYMBOLmethod_declaration : KEYWORD KEYWORD KEYWORD KEYWORD SYMBOL SYMBOL SYMBOL statement SYMBOLstatement : KEYWORD SYMBOL IDENTIFIER SYMBOL SYMBOL'
    
_lr_action_items = {'KEYWORD':([0,6,7,9,11,15,],[3,7,9,11,12,16,]),'$end':([1,2,10,],[0,-1,-2,]),'IDENTIFIER':([3,18,],[4,20,]),'SYMBOL':([4,5,8,12,13,14,16,17,19,20,21,22,],[5,6,10,13,14,15,18,19,-3,21,22,-4,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'class_declaration':([0,],[2,]),'method_declaration':([6,],[8,]),'statement':([15,],[17,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> class_declaration','program',1,'p_program','app.py',69),
  ('class_declaration -> KEYWORD IDENTIFIER SYMBOL SYMBOL method_declaration SYMBOL','class_declaration',6,'p_class_declaration','app.py',74),
  ('method_declaration -> KEYWORD KEYWORD KEYWORD KEYWORD SYMBOL SYMBOL SYMBOL statement SYMBOL','method_declaration',9,'p_method_declaration','app.py',79),
  ('statement -> KEYWORD SYMBOL IDENTIFIER SYMBOL SYMBOL','statement',5,'p_statement','app.py',84),
]
