import matplotlib.pyplot as plt
import numpy as np
from point import Point

fig = plt.figure()
p = Point(0, 0, "Point1")
resultats = p.determiner_triangle_while()

for point, coordonnees in resultats.items():
    print(f"{point}: ({coordonnees})")

point_A = resultats["point_A"]
point_B = resultats["point_B"]
point_C = resultats["point_C"]
point_D = resultats["point_D"]


mediatrice_AB = resultats["mediatrice_AB"]
mediatrice_BC = resultats["mediatrice_BC"]
mediatrice_AC = resultats["mediatrice_AC"]
mediatrice_AD = resultats["mediatrice_AD"]
mediatrice_BD = resultats["mediatrice_BD"]
mediatrice_DC = resultats["mediatrice_DC"]


pente_AC = resultats["pente_perpendiculaire_AC"]
pente_AB = resultats["pente_perpendiculaire_AB"]
pente_BC = resultats["pente_perpendiculaire_BC"]
pente_AD = resultats["pente_perpendiculaire_AD"]
pente_BD = resultats["pente_perpendiculaire_BD"]
pente_DC = resultats["pente_perpendiculaire_DC"]



plt.scatter(point_A._x, point_A._y, label="Point A")
plt.scatter(point_B._x, point_B._y, label="Point B")
plt.scatter(point_C._x, point_C._y, label="Point C")
plt.scatter(point_D._x, point_D._y, label="Point D")

plt.scatter(mediatrice_AB._x, mediatrice_AB._y, label="Médiatrice AB")
plt.scatter(mediatrice_BC._x, mediatrice_BC._y, label="Médiatrice BC")
plt.scatter(mediatrice_AC._x, mediatrice_AC._y, label="Médiatrice AC")


plt.axline((mediatrice_AC._x, mediatrice_AC._y), slope=pente_AC, color='red')
plt.axline((mediatrice_AB._x, mediatrice_AB._y), slope=pente_AB, color='purple')
plt.axline((mediatrice_BC._x, mediatrice_BC._y), slope=pente_BC, color='blue')
plt.axline((mediatrice_AD._x, mediatrice_AD._y), slope=pente_AD, color='green')
plt.axline((mediatrice_BD._x, mediatrice_BD._y), slope=pente_BD, color='orange')
plt.axline((mediatrice_DC._x, mediatrice_DC._y), slope=pente_DC, color='pink')


plt.plot([point_A._x, point_B._x], [point_A._y, point_B._y], 'k-')
plt.plot([point_A._x, point_C._x], [point_A._y, point_C._y], 'k-')
plt.plot([point_B._x, point_C._x], [point_B._y, point_C._y], 'k--')
plt.plot([point_A._x, point_D._x], [point_A._y, point_D._y], 'k:')
plt.plot([point_B._x, point_D._x], [point_B._y, point_D._y], 'k-.')
plt.plot([point_D._x, point_C._x], [point_D._y, point_C._y], 'k--')

plt.legend()
plt.plot([point_A._x, mediatrice_AB._x], [point_A._y, mediatrice_AB._y], 'k--')
plt.plot([point_C._x, mediatrice_DC._x], [point_C._y, mediatrice_DC._y], 'k--')
plt.axis('equal')
plt.show()


# point_C = resultats["point_C"]
# mediatrice_BC = resultats["mediatrice_BC"]
# mediatrice_AC = resultats["mediatrice_AC"]
# plt.scatter(point_A._x, point_A._y, label=point_A._name)
# plt.scatter(point_B._x, point_B._y, label=point_B._name)
# plt.scatter(point_C._x, point_C._y, label=point_C._name)
# plt.plot([point_B._x, point_C._x], [point_B._y, point_C._y], 'k-')
# plt.plot([point_A._x, point_C._x], [point_A._y, point_C._y], 'k-')
# plt.legend()
# plt.show()