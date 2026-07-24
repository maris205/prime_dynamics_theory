from gauge_route_review import minimal_missing_sets
def test_frontiers():
 rules=[(frozenset({'direct'}),'support'),(frozenset({'trace'}),'support'),(frozenset({'recurrence','base'}),'support'),(frozenset({'support','outward'}),'validated')]
 math=minimal_missing_sets(set(),rules,'support',{'direct','trace','recurrence','base','outward'});assert set(math)=={frozenset({'direct'}),frozenset({'trace'}),frozenset({'recurrence','base'})}
 valid=minimal_missing_sets(set(),rules,'validated',{'direct','trace','recurrence','base','outward'});assert set(valid)=={frozenset({'direct','outward'}),frozenset({'trace','outward'}),frozenset({'recurrence','base','outward'})}

