=================================================   
IBEE - Impost sobre Beguedes Ensucrades Envasades   
=================================================   

.. |badge1| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge2| image:: https://img.shields.io/badge/github-OCA%2Fodoo--B10-lightgray.png?logo=github
    :target: https://github.com/OCA/odoo-B10/tree/12.0/IBEE
    :alt: odoo-B10

Aquest mòdul implanta l'impost Català de Begudes Ensucrades.


**Taula de continguts**

.. contents::
   :local:

Utilització   
===========   

A la fitxa del article empleneu els camps IBEE amb el impost a aplicar i el camp litres IBEE amb la quantitat de litres per unitat de venda.   
Exemple: en una llauna de 33cl de cola marcarem 0,15 €/l d'impost i 0,33 litres per unitat   
Treurem el model 520 imprés des de Facturació -> Informes -> IBEE -> Model 520   


Registre de Versions
====================

12.0.0.1.0 (27/08/2022)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Creació Inicial del mòdul.   
* [ADD] Camps als articles per saber tipus de sucre i litres per unitat.   
* [ADD] Calcular impost en commades i factures.   
* [ADD] Informe de Model 520.   

12.0.0.1.1 (03/01/2023)
~~~~~~~~~~~~~~~~~~~~~~~

* [ADD] Dependencia de Dissenys_generics.   
* [ADD] Inerit de Dissenys_generics per mostrar-hi els valord d'IBEE si n'hi ha.    

Roadmap   
=======   

* Model 520 funcionant amb el mòdul date_range   
* Exportació a excel del Model 520   
* Valors dels impostos configurables de cara a futurs canvis de preus   

Registre d'errors
=================   

Podeu enviar errors a `GitHub Issues <https://github.com/B10Serveis/odoo-B10/issues>`_.

Crèdits
=======

Autors
~~~~~~

* Marc Tormo <marc@batista10.cat> (https://www.batista10.cat)

Contribuidors
~~~~~~~~~~~~~

* Marc Tormo <marc@batista10.cat> (https://www.batista10.cat)
* Pau Machetti Vallverdú <pmachetti@level4.es> (https://www.level4.es)

Altres   
~~~~~~  

El desenvolupament d'aquest mòdul ha estat impulsat i financiat per:

* Batista10 Serveis Informàtics



Aquest mòdul és part de `odoo-B10 <https://github.com/B10Serveis/odoo-B10/tree/12.0/IBEE>`_ project on GitHub.   
