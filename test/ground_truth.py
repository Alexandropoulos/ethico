# Expected verdicts: (Kantian, Utilitarian)

GROUND_TRUTH = {
    "trolley_problem": (False, True),
    "trolley_problem_permissible": (True, True),
    "fatman_trolley_problem": (False, True),
    "mixed_trolley": (True, True),
    "atom_bomb_trolley": (True, True),
    "disclose_burglar": (True, False),
    "disclose_doctor": (True, True),
    "lying_robot": (True, True),
    "indianer": (False, True),
    "slice_patch": (True, False),
    "flowers": (False, True),
    "flowers_permissible": (True, True),
    "hijacked_dilemma": (False, True),
    "strategic_bomber": (True, True),
    "terror_bomber": (False, True),
    "suffering": (True, False),
    "sadism": (False, False),
    "drugs": (False, False),
}

KANTIAN_TRUTH = {name: kantian for name, (kantian, utilitarian) in GROUND_TRUTH.items()}

UTILITARIAN_TRUTH = {
    name: utilitarian for name, (kantian, utilitarian) in GROUND_TRUTH.items()
}

UNIFIED_TRUTH = [
    (name, kantian, utilitarian)
    for name, (kantian, utilitarian) in GROUND_TRUTH.items()
]
