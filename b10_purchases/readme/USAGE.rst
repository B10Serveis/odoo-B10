To use this module, you need to:

**Instal·lació de field_encryption:**

El mòdul **field_encryption** és requereix per emmagatzemar i desxifrar el camp de contrasenya de proveïdor.

1. **Instal·lació**  

   - Ves a **Apps** i instal·la **Batista10 – Purchases**.  

2. **Configuració d’accés a la plataforma del proveïdor**  

   - Obre **Contacts → Partners** i selecciona un partner amb **Supplier Rank** > 0.  
   - Activa **Provider Access**.  
   - A la nova pestanya **Access**, introdueix:  

     - **Platform URL**  
     - **Username**  
     - **Password** (es desa encriptat; els usuaris del grup **Password Reader** només el veuen en mode lectura).  

   - Desa i comprova que el camp `x_provider_pwd_encrypted` s’omple al back-end.

3. **Gestió de grups d’usuaris exclusius**  

   - Crea o edita un usuari i assigna-li el grup **Password Manager**.  
   - Assigna-li també **Password Reader**: el sistema ha d’eliminar automàticament un dels dos per mantenir-los exclusius.  
   - Fes la prova equivalent modificant els grups des de **Settings → Users & Companies → Users** i **Settings → Users & Companies → Groups**.

4. **Enviar correus de pressupost i comanda**  

   - Crea una **Request for Quotation** o **Purchase Order** en estat **RFQ** / **Draft**.  
   - Prem **Send by Email**.  
   - Confirma que la plantilla carregada és la plantilla B10 corresponent (`presupost_email_template` o `pressupost_email_template` per RFQ, `comanda_email_template` per PO).  

5. **Impressió de PDF de pressupostos i comandes**  

   - Obre un RFQ i fes **Print → B10 Purchase Quotation** per generar el PDF amb el layout personalitzat.  
   - Obre una PO confirmada i fes **Print → B10 Purchase Order** per validar el report amb logo, dades d’empresa, i llistat de línies.  
