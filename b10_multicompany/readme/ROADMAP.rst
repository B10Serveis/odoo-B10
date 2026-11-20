* **Canvis posteriors a la creació de la compra**: B10 copia les línies quan
  genera la comanda de compra. Per si sol, no sincronitza els canvis posteriors
  de quantitat, preu, descompte, impostos o productes. Després de modificar una
  comanda, cal revisar la contrapartida i ajustar-la si correspon. Els impostos
  s'han de revisar segons les regles fiscals de cada empresa.
* **Amb el mòdul opcional de l'OCA**: es mantenen les seves regles de
  sincronització parcial. Els canvis de quantitat i les línies afegides a una
  compra confirmada poden actualitzar la venda vinculada si està confirmada i
  editable. En confirmar una venda vinculada, l'OCA pot actualitzar el preu net
  de la compra. Cal revisar l'estat i els imports de les dues comandes; aquestes
  regles no impliquen sincronització completa de tots els camps.
