import utils

NFA = utils.CreateNFA()
DFA = NFA.CreateEqeulvantDFA()
simpleDFA = DFA.MakeSimpleDFA()

GNFA = utils.GNFA(NFA)

print(utils.FindRejex(GNFA))

# {1,2,3,4}
# {a,b}
# 8
# 1,2,a
# 2,2,a
# 2,3,b
# 3,3,a
# 3,3,b
# 1,4,b
# 4,4,b
# 4,2,a
# {3}
