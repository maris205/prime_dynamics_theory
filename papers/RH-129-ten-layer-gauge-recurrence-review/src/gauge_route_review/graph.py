"""Finite monotone proof-frontier enumeration."""
from __future__ import annotations
import itertools

def _closure(proved:set[str],rules:list[tuple[frozenset[str],str]])->set[str]:
 closed=set(proved);changed=True
 while changed:
  changed=False
  for antecedent,consequent in rules:
   if antecedent<=closed and consequent not in closed:closed.add(consequent);changed=True
 return closed
def minimal_missing_sets(proved:set[str],rules:list[tuple[frozenset[str],str]],target:str,candidates:set[str])->list[frozenset[str]]:
 if target in _closure(proved,rules):return [frozenset()]
 winners=[];ordered=sorted(candidates)
 for size in range(1,len(ordered)+1):
  for combo in itertools.combinations(ordered,size):
   choice=frozenset(combo)
   if any(old<=choice for old in winners):continue
   if target in _closure(proved|set(choice),rules):winners.append(choice)
 return sorted(winners,key=lambda x:(len(x),sorted(x)))

