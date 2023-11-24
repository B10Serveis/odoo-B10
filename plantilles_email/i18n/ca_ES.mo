��          |      �          �*  !  �*  �+  �*  uV  @   %�  0   f�  4   ��  !   ́  #   �  $   �  R   7�  B   ��    ͂  �)  �  �)  ��  �)  |�  @   Q 2   � 5   �    �        & R   C D   �                            	             
                 <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Invoice from </span>
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Dear 
                                                                <t t-out="object.partner_id.name + ',' or ','" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    You have a new invoice available:
                                                                <br/>
                                                                <p style="margin-left: 16px">
                                                                    Invoice number: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br/>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Amount invoiced: 
                                                                    <t t-out="format_amount(object.amount_total_signed, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Invoice date: 
                                                                    <t t-out="format_date(object.date) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.user_id.company_id.name"/>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="object.user_id.company_id.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ object.user_id.company_id.email }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="object.user_id.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ object.user_id.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                According to the GDPR, we inform you that we will process your personal data in order to carry out administrative, accounting and fiscal management. Data
                                                                proportionately, the time required by a legal obligation will be retained and will not be transferred to third parties except legal provision required, or if necessary, prior consent of
                                                                The interested party. It will be able to exercise the following rights on its personal data: right of access, rectification, erasure, oblate, limitation, opposition, portability and to withdraw the
                                                                consent given, to the address indicated in this document. In addition, it will be able to contact the competent supervisory authority in the field of data protection by
                                                                get additional information or file a complaint.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Order from </span>
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Dear 
                                                                <t t-out="object.partner_id.name + ',' or ','" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    You have a new order available:
                                                                <br/>
                                                                <p style="margin-left: 16px">
                                                                    Order number: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br/>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Amount Ordered: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Order date: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.user_id.company_id.name"/>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="object.user_id.company_id.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ object.user_id.company_id.email }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="object.user_id.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ object.user_id.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                According to the GDPR, we inform you that we will process your personal data in order to carry out administrative, accounting and fiscal management. Data
                                                                proportionately, the time required by a legal obligation will be retained and will not be transferred to third parties except legal provision required, or if necessary, prior consent of
                                                                The interested party. It will be able to exercise the following rights on its personal data: right of access, rectification, erasure, oblate, limitation, opposition, portability and to withdraw the
                                                                consent given, to the address indicated in this document. In addition, it will be able to contact the competent supervisory authority in the field of data protection by
                                                                get additional information or file a complaint.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Order from </span>
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Dear 
                                                                <t t-out="object.partner_id.name + ',' or ','" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    You have a new quotation available:
                                                                <br/>
                                                                <p style="margin-left: 16px">
                                                                    Quotation number: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br/>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Amount Quoted: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Quotation date: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.user_id.company_id.name"/>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="object.user_id.company_id.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ object.user_id.company_id.email }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="object.user_id.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ object.user_id.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                According to the GDPR, we inform you that we will process your personal data in order to carry out administrative, accounting and fiscal management. Data
                                                                proportionately, the time required by a legal obligation will be retained and will not be transferred to third parties except legal provision required, or if necessary, prior consent of
                                                                The interested party. It will be able to exercise the following rights on its personal data: right of access, rectification, erasure, oblate, limitation, opposition, portability and to withdraw the
                                                                consent given, to the address indicated in this document. In addition, it will be able to contact the competent supervisory authority in the field of data protection by
                                                                get additional information or file a complaint.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         Invoice_{{ (object.ref or object.name or '').replace('/','_') }} Order_{{ (object.name or '').replace('/','_') }} Quotation_{{ (object.name or '').replace('/','_') }} Standard - Invoice Email Template Standard - Quotation Email Template Standard - Sale Order Email Template {{ object.company_id.name }} Invoice ref. {{ object.name or object.ref or 'n/a' }} {{ object.company_id.name }} Order ref. {{ object.name or 'n/a' }} Project-Id-Version: Odoo Server 15.0
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2023-11-24 11:55+0100
Last-Translator: 
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: 
Language: ca_ES
X-Generator: Poedit 2.4.2
 <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Factura de </span>
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Benvolgut/da 
                                                                <t t-out="object.partner_id.name + ',' or ','" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    Teniu una factura nova disponible:
                                                                <br/>
                                                                <p style="margin-left: 16px">
                                                                    Número de factura: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br/>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Import facturat: 
                                                                    <t t-out="format_amount(object.amount_total_signed, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Data factura: 
                                                                    <t t-out="format_date(object.date) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.user_id.company_id.name"/>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="object.user_id.company_id.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ object.user_id.company_id.email }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="object.user_id.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ object.user_id.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                D’acord amb l’establert al RGPD, l’informem que tractarem les seves dades personals amb la finalitat de realitzar la gestió administrativa, comptable i fiscal. Les dades
proporcionades es conservaran el temps exigible per una obligació legal i no seran cedides a tercers excepte previsió legal exigible, o en el seu cas, previ consentiment de
l’interessat. Podrà exercir els següents drets sobre les seves dades personals: dret d’accés, rectificació, supressió, oblit, limitació, oposició, portabilitat i a retirar el
\consentiment prestat, a l’adreça assenyalada en el present document. A més, podrà adreçar-se a l’autoritat de Control competent en matèria de Protecció de Dades per
obtenir informació addicional o presentar una reclamació.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Comanda de </span>
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Benvolgut/da 
                                                                <t t-out="object.partner_id.name + ',' or ','" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    Teniu una nova comanda disponible:
                                                                <br/>
                                                                <p style="margin-left: 16px">
                                                                    Número comanda: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br/>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Import comanda: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Data comanda: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.user_id.company_id.name"/>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="object.user_id.company_id.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ object.user_id.company_id.email }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="object.user_id.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ object.user_id.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                D’acord amb l’establert al RGPD, l’informem que tractarem les seves dades personals amb la finalitat de realitzar la gestió administrativa, comptable i fiscal. Les dades
proporcionades es conservaran el temps exigible per una obligació legal i no seran cedides a tercers excepte previsió legal exigible, o en el seu cas, previ consentiment de
l’interessat. Podrà exercir els següents drets sobre les seves dades personals: dret d’accés, rectificació, supressió, oblit, limitació, oposició, portabilitat i a retirar el
\consentiment prestat, a l’adreça assenyalada en el present document. A més, podrà adreçar-se a l’autoritat de Control competent en matèria de Protecció de Dades per
obtenir informació addicional o presentar una reclamació.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         <table style="padding-top: 16px; background-color: white; font-family:Verdana, Arial,sans-serif; color: #454748; width: 100%; border-collapse:separate;" cellspacing="0" cellpadding="0" border="0">
                <tbody>
                    <tr>
                        <td align="center">
                            <table t-attf-style="padding: 16px; color: #454748; border-collapse:separate; background-color: #F1F1F1" width="590" cellspacing="0" cellpadding="0" border="0">
                                <tbody>

                                    <!-- HEADER -->
                                    <tr style="">
                                        <td style="min-width: 590px;" align="center">
                                            <table t-attf-style="min-width: 590px; padding: 0px 8px 0px 8px; border-bottom: solid gray 2px; border-collapse:separate; background-color: {{ object.user_id.company_id.primary_color or 'gray'}}" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td valign="middle" style="padding: 16px; font-size: 20px; font-weight: bold; color: white;">
                                                            <span>Pressupost de </span>
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- CONTENT -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: white; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="font-size: 13px; padding: 16px;" valign="top">
                                                            <div>
                                                                    Benvolgut/da 
                                                                <t t-out="object.partner_id.name + ',' or ','" data-oe-t-inline="true" contenteditable="false">
                                                                </t>
                                                                <br/>
                                                                    Teniu un pressupost nou disponible:
                                                                <br/>
                                                                <p style="margin-left: 16px">
                                                                    Número pressupost: 
                                                                    <span style="font-weight: bold;">
                                                                        <t t-out="object.name or 'n/a'" data-oe-t-inline="true" contenteditable="false">
                                                                        </t>
                                                                    </span>
                                                                    <br/>
                                                                    Client: 
                                                                    <t t-out="object.partner_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Import pressupost: 
                                                                    <t t-out="format_amount(object.amount_total, object.currency_id) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                    <br/>
                                                                    Data pressupost: 
                                                                    <t t-out="format_date(object.date_order) or ''" data-oe-t-inline="true" contenteditable="false">
                                                                    </t>
                                                                </p>
                                                            </div>
                                                        </td>
                                                        <!-- LOGO -->
                                                        <td valign="top" align="right">
                                                            <img t-attf-src="/logo.png?company={{ object.user_id.company_id.id }}" style="padding: 0px; margin: 16px; height: auto; width: 100px;" t-att-alt="object.user_id.company_id.name"/>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>

                                    <!-- FOOTER -->
                                    <tr>
                                        <td style="min-width: 590px;" align="center">
                                            <table style="min-width: 590px; background-color: #F1F1F1; font-size: 11px; margin-top: 16px; padding: 0px 8px 0px 8px; border-collapse:separate;" width="590" cellspacing="0" cellpadding="0" border="0">
                                                <tbody>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.signature or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 14px; font-weight: bold;">
                                                            <t t-out="object.user_id.company_id.name or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="opacity: 0.7;" valign="middle" align="left">
                                                            <t t-out="object.user_id.company_id.phone or ''" data-oe-t-inline="true" contenteditable="false">
                                                            </t>
                                                            <t t-if="object.user_id.company_id.email" data-oe-t-group="0" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'mailto:%s' % {{ object.user_id.company_id.email }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.email or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                            <t t-if="object.user_id.company_id.website" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true">
                                                                    |
                                                                <a t-attf-href="'%s' % {{ object.user_id.company_id.website }}" style="text-decoration:none; color: #454748;" t-out="object.user_id.company_id.website or ''" contenteditable="false">
                                                                </a>
                                                            </t>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td valign="middle" align="left" style="font-size: 10px; text-decoration:none; color: #454748; padding-top:10px;">
                                                                D’acord amb l’establert al RGPD, l’informem que tractarem les seves dades personals amb la finalitat de realitzar la gestió administrativa, comptable i fiscal. Les dades
proporcionades es conservaran el temps exigible per una obligació legal i no seran cedides a tercers excepte previsió legal exigible, o en el seu cas, previ consentiment de
l’interessat. Podrà exercir els següents drets sobre les seves dades personals: dret d’accés, rectificació, supressió, oblit, limitació, oposició, portabilitat i a retirar el
\consentiment prestat, a l’adreça assenyalada en el present document. A més, podrà adreçar-se a l’autoritat de Control competent en matèria de Protecció de Dades per
obtenir informació addicional o presentar una reclamació.
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
         Factura_{{ (object.ref or object.name or '').replace('/','_') }} Comanda_{{ (object.name or '').replace('/','_') }} Pressupost_{{ (object.name or '').replace('/','_') }} Estandard - Factura Estandard - Pressupost Estandard - Comanda de venda {{ object.company_id.name }} Factura ref. {{ object.name or object.ref or 'n/a' }} {{ object.company_id.name }} Comanda ref. {{ object.name or 'n/a' }} 