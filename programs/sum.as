# Estados: {q0, q1, q2, q3, HALT}
# Alfabeto de cinta: {_, 0, 1, X}   // _ = blanco

# Transiciones:

(q0,0) - (q0,0,>)
(q0,1) - (q1,X,>)
(q0,_) - (HALT,_,=)

(q1,0) - (q1,0,>)
(q1,1) - (q1,1,>)
(q1,_) - (q2,_,>)

(q2,_) - (q3,1,<)
(q2,1) - (q2,1,>)

(q3,0) - (q3,0,<)
(q3,1) - (q3,1,<)
(q3,_) - (q3,_,<)
(q3,X) - (q0,X,>)