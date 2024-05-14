def calc_score(to_score, reference, note_length):
    score = 0
    if len(to_score) == 0 or len(reference) == 0:
        return 0
    delay = to_score[0][2]
    for i in range(len(to_score)):
        to_score[i][2] = to_score[i][2] - delay
    delay = reference[0][2]
    for i in range(len(reference)):
        reference[i][2] = reference[i][2] - delay
    print(f"to_score:\n{to_score}\n")
    print(f"reference:\n{reference}\n")
    for i in range(len(to_score)):
        to_score[i][2] /= note_length
    for elem_to_score in to_score:
        for elem_reference in reference:
            if (
                elem_to_score[0] == elem_reference[0]
                and elem_to_score[1] == elem_reference[1]
                and abs(elem_to_score[2] - elem_reference[2]) <= 2000
            ):
                reference.remove(elem_reference)
                score += 100
                break
        else:
            score -= 50
    return max(score, 0)
