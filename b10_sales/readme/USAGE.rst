Per fer servir aquest mòdul:

#. Instal·la **b10_sales** des de Apps.  
#. Ves a **Sales → Orders** i utilitza el filtre **Expired** per veure pressupostos caducats.  
#. Obre o crea una **Sales Order** i trobaràs el checkbox **Show product image** sota **Payment Mode**.  
#. Per imprimir:  

   - **Pressupost Estandard**  
   - **Pressupost Estandard S/T**  
   - **Comanda Estandard**  
   - **ProForma Estandard**  

   des del menú **Print**.

#. Enviar per Email  

   - Obre un Pressupost i clica **Send by Email**: s’auto‐selecciona la plantilla **Standard - Quotation Email Template**.  
   - Obre una Comanda i clica **Send by Email**: s’auto‐selecciona la plantilla **Standard - Sale Order Email Template**.  
   - Obre una ProForma i clica **Send by Email**: s’auto‐selecciona la plantilla **Standard - Proforma Email Template**.  

#. Classificacions de Marges:  

   - Ves a: Vendes > Configuració > Productes > Classificacions de Marges
   - Crea noves classificacions
   - Assigna classificacions als teus productes

Correcció dels noms dels informes en instal·lacions existents
-----------------------------------------------------------

La versió 18.0.1.9.1 incorpora les traduccions corregides dels quatre informes de venda
en català i castellà, amb el prefix «B10 -». Si una instal·lació conserva
noms incorrectes, cal importar ``b10_sales/i18n/ca_ES.po`` i
``b10_sales/i18n/es.po`` per als idiomes corresponents, marcant
«Sobreescriure termes existents». Una actualització ordinària del mòdul pot
conservar les traduccions incorrectes ja desades a la base de dades.
