from matplotlib import pyplot as plt
from diagramme_voronoi import Diagramme_Voronoi

diagramme_voronoi = Diagramme_Voronoi()
diagramme_voronoi.parcourir_donnees() 
print("Points chargés :", len(diagramme_voronoi.liste_points))
diagramme_voronoi.calculer_delauney()

print("Triangles de Delaunay calculés :", len(diagramme_voronoi.liste_triangles))
print("Liste des triangles :")
for triangle in diagramme_voronoi.liste_triangles:
    print(triangle)
triangle_valide = diagramme_voronoi.triangle_valide(diagramme_voronoi.liste_triangles[0], diagramme_voronoi.liste_points[0], diagramme_voronoi.liste_points[1], diagramme_voronoi.liste_points[2])
print("Le triangle est-il valide ?", triangle_valide)

fig = plt.figure(figsize=(6, 6))

#lie les cercles circonscrits des triangles qui on un segment commun
for i in range(len(diagramme_voronoi.liste_triangles)):
    for j in range(i + 1, len(diagramme_voronoi.liste_triangles)):
        t1 = diagramme_voronoi.liste_triangles[i]
        t2 = diagramme_voronoi.liste_triangles[j]
        segment_commun = t1.partage_un_segment(t2)
        if segment_commun is not None:
            plt.plot([t1._cercle_circonscrit._x, t2._cercle_circonscrit._x],
                     [t1._cercle_circonscrit._y, t2._cercle_circonscrit._y], 'b-', linewidth=2)

#Tracer les demi-droites de Voronoi pour les segments du bord
for triangle in diagramme_voronoi.liste_triangles:
    for seg in [triangle._segment1, triangle._segment2, triangle._segment3]:
        if triangle.segment_est_sur_le_bord(seg, diagramme_voronoi.liste_triangles):

            centre = triangle._cercle_circonscrit #Trouver le centre du cercle circonscrit du triangle
            sommet_oppose = triangle.trouver_sommet_oppose(seg)

            mx = (seg._PointA._x + seg._PointB._x) / 2
            my = (seg._PointA._y + seg._PointB._y) / 2

            perp_x = -(seg._PointB._y - seg._PointA._y) #y car perp_x = -dy => (dx,dy) => (-dy, dx)
            perp_y = seg._PointB._x - seg._PointA._x #dx car perp_y = dx

            if sommet_oppose is not None:
                if (sommet_oppose._x - mx) * perp_x + (sommet_oppose._y - my) * perp_y > 0: #même sens que le sommet opposé
                    perp_x, perp_y = -perp_x, -perp_y

            # Tracer vers l'extérieur du triangle (50 c'est pour dépasser les limites du graphique)
            plt.plot([centre._x, centre._x + perp_x * 50],
                     [centre._y, centre._y + perp_y * 50], 'b-', linewidth=2)


for i, point in enumerate(diagramme_voronoi.liste_points):
    plt.scatter(point._x, point._y, color="grey", label=f"P{i+1} ({point._x}, {point._y})")
    plt.annotate(f"P{i+1}", (point._x, point._y), textcoords="offset points", xytext=(-3, 8), fontsize=9)

plt.title("Diagramme de Voronoï")
plt.xlim(-5, 25)
plt.ylim(-5, 35)
plt.gca().set_aspect('equal', adjustable='datalim')
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.savefig("phase1/data/diagramme_voronoi_groupeD.png")
plt.savefig("phase1/data/diagramme_voronoi_groupeD.svg")
plt.show()