Aquest mòdul afegeix plantilles PDF i funcionalitats addicionals per a vendes:  

* Filtre “Expired” de pressupostos  
* Checkbox “Show product image” al formulari  
* Selecció de diari de pagament al formulari (pestanya d'altra informació), per a incloure'n l'IBAN als dissenys  
* Dissenys per a Pressupost, Pressupost S/T, Comanda i ProForma  
* Plantilles Email per a Pressupost, Comanda i ProForma  

A més, aquest mòdul està dissenyat per ampliar el càlcul del preu de venda a Odoo.

Afegeix un nou model 'Classificacions de Marges' vinculat a les variants de producte.

Una classificació de marge té un camp 'Marge de Benefici' i camps addicionals per gestionar
el mètode de càlcul, com en el model d'ítem de llista de preus (Taxa de Markup, Mètode de Redondeig i Camps de Càrrega)

Si el producte té una classificació de marge definida i el preu teòric no és
el mateix que el preu de venda, es mostra un camp addicional 'Preu Teòric',
basat en la Classificació de Marge i un botó està disponible per
canviar el preu de venda.

.. image:: https://raw.githubusercontent.com/OCA/margin-analysis/12.0/product_margin_classification/static/description/product_product_form.png

En el formulari de Classificació de marge, l'usuari pot canviar els camps de càlcul.
(Marge, Mètode de Redondeig, ...)
Tres botons estan disponibles per aplicar els preus teòrics:

* a tots els productes,
* només per als productes que són massa cars
* només per als productes que són massa barats

.. image:: https://raw.githubusercontent.com/OCA/margin-analysis/12.0/product_margin_classification/static/description/margin_classification_form.png

Clicant en els botons intel·ligents a la part dreta del formulari,
tots els productes es mostraran, i l'usuari pot canviar fàcilment els preus

.. image:: https://raw.githubusercontent.com/OCA/margin-analysis/12.0/product_margin_classification/static/description/product_product_tree_incorrect_price.png

L'usuari també pot veure fàcilment els productes amb marges incorrectes en les vistes d'arbre de classificació de marges:

.. image:: https://raw.githubusercontent.com/OCA/margin-analysis/12.0/product_margin_classification/static/description/margin_classification_tree.png
